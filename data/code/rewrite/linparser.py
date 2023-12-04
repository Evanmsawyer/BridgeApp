# update of linparser that ignores newlines and uses a new parsing method
# TODO: ISSUE: if a failure occurs during a write to CSVs, we get inconsistent information
import glob
import sys
import os
import parser_classes
import json
import mysql.connector

r_id = 0; b_id = 0; t_id = 0; num_read = 1
if os.path.isfile("parser_config.json"):
    with open("parser_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    config = config["parser"]
    r_id = config["r_id"]
    b_id = config["b_id"]
    t_id = config["t_id"]

def read_file(filename: str):
    if not (os.path.isfile(filename)): raise Exception("invalid path")
    # open file
    with open(filename, mode='r', encoding='utf-8') as fd:
        # load in all lines
        file = ""
        for line in fd:
            file += line
        file = file.replace("\n", "")
        file = file.split("|")
        # get header
        if file[0] != "vg": raise Exception("invalid header syntax")
        header = file[1]
        # get players
        try: players = file[(file.index("pn") + 1)]
        except ValueError: raise Exception("cannot find player list")
        # construct round object
        round = parser_classes.Round(header, players)
        # "seek" to first instance of "qx"
        file = file[file.index("qx"):]
        board = None
        # loop through file
        while True:
            # check if this is the last bid phase, break if true
            try: i = file.index("qx", 1)
            except ValueError: break
            # create board if it doesn't exist
            if board is None:
                board = parser_classes.Board(file[:i])
                round.boards += [board]
            # add second table to board, then score board and set to None
            else:
                board.add_table(file[:i])
                board.score_board()
                board = None
            # "seek" to next instance of "qx"
            file = file[i:]
        # add final table to final board
        if board is not None:
            board.add_table(file)
        # check that number of boards and tables are valid
        else: raise Exception("invalid number of tables")
        # score all boards
        for board in round.boards: 
            board.score_board()
            if board.tables[0].board_number != board.tables[1].board_number:
                raise Exception("mismatched table pairings")
        return round

def insert_data(round: parser_classes.Round, db: mysql.connector.MySQLConnection):
    # set up cursor object
    cursor = db.cursor()
    # get round ID
    cursor.execute("SELECT max(RoundID) FROM BridgeDB.RoundID")
    r_id = cursor.fetchall()[0][0] + 1
    # get table ID
    cursor.execute("SELECT max(TableID) FROM BridgeDB.TableEntity")
    t_id = cursor.fetchall()[0][0] + 1
    # get board ID
    cursor.execute("SELECT max(BoardID) FROM BridgeDB.Board")
    b_id = cursor.fetchall()[0][0] + 1
    # start transaction
    try:
        db.autocommit = False
        db.start_transaction()
        # begin insertions
        for team in round.teams:
            name = team.team_name
            # teams
            cursor.execute("IF " + name + " NOT IN (SELECT * FROM BridgeDB.Team)"
                        "INSERT INTO BridgeDB.Team VALUE (" + name + ");"
                        "ENDIF")
            
            for player in team.players:
                # players
                cursor.execute("IF NOT EXISTS (SELECT * FROM BridgeDB.Player"
                            "WHERE Player.Name = \"" + player + "\" AND Player.TeamName = \"" + name + "\")"
                            "INSERT INTO BridgeDB.Player VALUES (\"" + player + "\",\"" + name + "\");"
                            "ENDIF")
        # round
        cursor.execute("INSERT INTO BridgeDB.Round"
                       "VALUES (" + str(r_id) + "," + str(round) + ")")
        
        for board in round.boards:
            # board
            cursor.execute("INSERT INTO BridgeDB.Board"
                           "VALUES(" + str(b_id) + "," + str(r_id) + str(board) + ")")
            # hand
            for hand in board.hands:
                cursor.execute("INSERT INTO BridgeDB.Hands"
                               "VALUES (" + str(b_id) + "," + str(hand) + ")")
            # tables
            table1 = board.tables[0]
            table2 = board.tables[1]
            # turn off key constraints
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            # table 1
            cursor.execute("INSERT INTO BridgeDB.TableEntity"
                           "VALUES(" + str(t_id) + "," + str(t_id + 1) + "," + str(b_id) + "," + str(table1) + ")")
            # table 2
            cursor.execute("INSERT INTO BridgeDB.TableEntity"
                           "VALUES(" + str(t_id + 1) + "," + str(t_id) + "," + str(b_id) + "," + str(table2) + ")")
            # turn key constraints back on
            cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            # trick
            for trick in table1.tricks:
                cursor.execute("INSERT INTO BridgeDB.Trick"
                               "VALUES(" + str(trick.num) + "," + str(t_id) + "," + str(trick) + ")")
            for trick in table2.tricks:
                cursor.execute("INSERT INTO BridgeDB.Trick"
                               "VALUES(" + str(trick.num) + "," + str(t_id + 1) + "," + str(trick) + ")")
            # plays table
            for player in round.player_list:
                i = round.player_list.index(player)
                team = str(round.teams[0]) if player in round.teams[0].members else str(round.teams[1])
                pos = str((i % 4) + 1)
                name = '\"' + player + '\"'
                if i > 3:
                    cursor.execute("INSERT INTO BridgeDB.PlaysTable"
                                   "VALUES (" + str(t_id + 1) + "," + pos + "," + name + "," + team + ")")
                else:
                    cursor.execute("INSERT INTO BridgeDB.PlaysTable"
                                   "VALUES (" + str(t_id) + "," + pos + "," + name + "," + team + ")")
            # commit
            db.commit()
    except mysql.connector.Error as error:
        db.rollback()
        raise error

def write_header(name, fd):
    # creates headers for csv files
    match name:
        # round.csv
        case "round.csv":
            print("\"Round ID\",\"Tournament Name\",\"Team One\",\"Team Two\"", file=fd)
        # board.csv
        case "board.csv":
            print("\"Board ID\",\"Round ID\",\"Dealer\",\"Vulnerability\",\"Team One IMPs\",\"Team Two IMPs\"", file=fd)
        # table.csv
        case "table.csv":
            print("\"Table ID\",\"Paired ID\",\"Board ID\",\"Bid Phase\",\"First Bid\",\"Last Bid\",\"Result\",\"Raw Score\"", file=fd)
        # hand.csv
        case "hand.csv":
            print("\"Board ID\",\"Position\",\"Spades\",\"Hearts\",\"Diamonds\",\"Clubs\",\"High Card Points\"", file=fd)
        # trick.csv
        case "trick.csv":
            print("\"Trick Number\",\"Table ID\",\"First Seat\",\"Winning Seat\",\"Play\"", file=fd)
        # team.csv
        case "team.csv":
            print("\"Team Name\"", file=fd)
        # player.csv
        case "player.csv":
            print("\"Player Name\",\"Team Name\"", file=fd)
        # plays_table.csv
        case "plays_table.csv":
            print("\"Table ID\",\"Seat\",\"Player Name\",\"Team Name\"", file=fd)

def write_csv(round: parser_classes.Round):
    global r_id, b_id, t_id
    # open files
    with (open("round.csv", "a", encoding="UTF-8") as round_csv, open("board.csv", "a", encoding="UTF-8") as board_csv,
          open("table.csv", "a", encoding="UTF-8") as table_csv, open("hand.csv", "a", encoding="UTF-8") as hand_csv,
          open("trick.csv", "a", encoding="UTF-8") as trick_csv, open("team.csv", "a", encoding="UTF-8") as team_csv,
          open("player.csv", "a", encoding="UTF-8") as player_csv, open("plays_table.csv", "a", encoding="UTF-8") as plays_csv):
        # write to round.csv (round_id, tournament_name, team_one_name, team_two_name)
        print(r_id, round, file=round_csv, sep=",")

        # write to board.csv (board_id, round_id, dealer, vuln, team_one_imps, team_two_imps)
        for board in round.boards:
            print(b_id, r_id, board, file=board_csv, sep=",")
            # write to hand.csv (board_id, position, spades, hearts, diamonds, clubs, hcp)
            for hand in board.hands:
                print(b_id, hand, file=hand_csv, sep=",")

            # write to table.csv (table_id, paired_id, board_id, bid_phase, first_bid, last_bid, result, declarer_score)
            table_1 = board.tables[0]
            table_2 = board.tables[1]
            print(t_id, (t_id + 1), b_id, table_1, file=table_csv, sep=",")
            print((t_id + 1), t_id, b_id, table_2, file=table_csv, sep=",")

            # write to trick.csv (num, t_id, play, start_pos)
            for trick in table_1.tricks:
                print(trick.num, t_id, trick, file=trick_csv, sep=",")
            for trick in table_2.tricks:
                print(trick.num, (t_id + 1), trick, file=trick_csv, sep=",")
            
            # write to plays_table.csv (table_id, seat, player_name, team_name)
            for player in round.player_list:
                i = round.player_list.index(player)
                team = round.teams[0] if player in round.teams[0].members else round.teams[1]
                pos = str((i % 4) + 1)
                name = '\"' + player + '\"'
                if(i > 3):
                    print((t_id + 1), pos, name, team, sep=",", file=plays_csv)
                else:
                    print(t_id, pos, name, team, sep=",", file=plays_csv)
            b_id += 1
            t_id += 2
            
        # write to team.csv (team_name)
        for team in round.teams:
            print(team, file=team_csv)
            # write to player.csv (player_name, team_name)
            for player in team.members:
                p_string = '\"' + player + '\"'
                print(p_string, team, sep=',', file=player_csv)
        r_id += 1
    global num_read
    print(num_read)
    num_read += 1

def main():
    # read files in and write to CSVs
    # if parse arguments, if given
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            # if the argument is a directory, search the directory
            if os.path.isdir(arg):
                for f in glob.iglob(arg + "*.lin"):
                    try:
                        print("Starting", f)
                        round = read_file(f)
                        write_csv(round)
                    except Exception as err:
                        print("Error on file " + f + ":", err)
                    print("Finished", f)
            #if the argument is a file, read it as a .lin file
            elif os.path.isfile(arg):
                try:
                    print("Starting", arg)
                    round = read_file(arg)
                    write_csv(round)
                except Exception as err:
                    print("Error on argument " + arg + ":", err)
                print("Finished", arg)
    # if no arguments were given, look for files in working directory
    else:
        for f in glob.iglob("*.lin"):
            print("Starting", f)
            try:
                round = read_file(f)
                write_csv(round)
            except Exception as err:
                print("Error on file " + f + ":", err)
            print("Finished", f)
    # remove duplicates from CSVs
    print("Removing duplicates")
    try:
        for f in glob.iglob("*.csv"):
            l_set = set()
            with open(f, mode="r", encoding="UTF-8") as fd:
                for line in fd:
                    l_set.add(line)
            with open(f, mode="w", encoding="UTF-8") as fd:
                write_header(f, fd)
                for line in l_set:
                    print(line, file=fd, end="")
    except Exception as err:
        print("Error removing duplicate tuples from CSVs:", err)
    print("Done")
   
    with open("config_parser.json", mode="w", encoding="UTF-8") as f:
        s = "{\n  \"parser\": {\n    \"r_id\": " + str(r_id) + ",\n    \"b_id\": "+ str(b_id) +",\n    \"t_id\": " + str(t_id) + "\n  }\n}"
        f.write(s)

if __name__ == "__main__":
    main()