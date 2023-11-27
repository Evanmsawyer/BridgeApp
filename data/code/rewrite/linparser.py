#Update of linparser that ignores newlines and uses a new parsing method
import glob
import sys
import os
import parser_classes
import json

r_id = 0; b_id = 0; t_id = 0; num_read = 1
if os.path.isfile("parser_config.json"):
    with open("parser_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    config = config["parser"]
    r_id = config["r_id"]
    b_id = config["b_id"]
    t_id = config["t_id"]


def read_file(filename):
    if not (os.path.isfile(filename)): raise ValueError
    #open file
    with open(filename, mode='r', encoding='utf-8') as fd:
        #Load in all lines
        file = ""
        for line in fd:
            file += line
        file = file.replace("\n", "")
        file = file.split("|")
        if file[0] != "vg": raise RuntimeError
        header = file[1]


def write_csv(round: parser_classes.Round):
    global r_id, b_id, t_id
    #open files
    with (open("round.csv", "a", encoding="UTF-8") as round_csv, open("board.csv", "a", encoding="UTF-8") as board_csv,
          open("table.csv", "a", encoding="UTF-8") as table_csv, open("hand.csv", "a", encoding="UTF-8") as hand_csv,
          open("trick.csv", "a", encoding="UTF-8") as trick_csv, open("team.csv", "a", encoding="UTF-8") as team_csv,
          open("player.csv", "a", encoding="UTF-8") as player_csv, open("plays_table.csv", "a", encoding="UTF-8") as plays_csv):
        #write to round.csv (round_id, tournament_name, team_one_name, team_two_name)
        print(r_id, round, file=round_csv, sep=",")

        #write to board.csv (board_id, round_id, dealer, vuln)
        for board in round.boards:
            print(b_id, r_id, board, file=board_csv, sep=",")
            #write to hand.csv (hand_id, board_id, position, spades, hearts, diamonds, clubs, hcp)
            for hand in board.hands:
                print(b_id, hand, file=hand_csv, sep=",")

            #write to table.csv (table_id, board_id, paired_id, bid_phase, last_bid, result, declarer_score)
            table_1 = board.tables[0]
            table_2 = board.tables[1]
            print(t_id, (t_id + 1), b_id, table_1, file=table_csv, sep=",")
            print((t_id + 1), t_id, b_id, table_2, file=table_csv, sep=",")

            #write to trick (num, t_id, play, start_pos)
            for trick in table_1.tricks:
                print(trick.num, t_id, trick, file=trick_csv, sep=",")
            for trick in table_2.tricks:
                print(trick.num, (t_id + 1), trick, file=trick_csv, sep=",")
            
            #write to plays_table.csv
            for player in round.player_list:
                i = round.player_list.index(player)
                team = round.teams[0] if player in round.teams[0].members else round.teams[1]
                pos = '\"' + parser_classes.pos_dic[(i % 4) + 1] + '\"'
                name = '\"' + player + '\"'
                if(i > 3):
                    print((t_id + 1), pos, name, team, sep=",", file=plays_csv)
                else:
                    print(t_id, pos, name, team, sep=",", file=plays_csv)
                    
            b_id += 1
            t_id += 2
            
        #write to team.csv
        for team in round.teams:
            print(team, file=team_csv)
            #write to player.csv
            for player in team.members:
                p_string = '\"' + player + '\"'
                print(p_string, team, sep=',', file=player_csv)
        r_id += 1
    global num_read
    print(num_read)
    num_read += 1

def main():
    #read files in and write to CSVs
    print("Arguments", sys.argv)
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if os.path.isdir(arg):
                for f in glob.iglob(arg + "*.lin"):
                    try:
                        print("Starting", f)
                        round = read_file(f)
                        write_csv(round)
                    except Exception as err:
                        print("Error on file " + f + ":", err)
                    print("Finished", f)
            elif os.path.isfile(arg):
                try:
                    print("Starting", arg)
                    round = read_file(arg)
                    write_csv(round)
                except Exception as err:
                    print("Error on argument " + arg + ":", err)
                print("Finished", arg)
    else:
        for f in glob.iglob("*.lin"):
            print("Starting", f)
            try:
                round = read_file(f)
                write_csv(round)
            except Exception as err:
                print("Error on file " + f + ":", err)
            print("Finished", f)
    #remove duplicates from CSVs
    print("Removing duplicates")
    try:
        for f in glob.iglob("*.csv"):
            l_set = set()
            with open(f, mode="r", encoding="UTF-8") as fd:
                for line in fd:
                    l_set.add(line)
            with open(f, mode="w", encoding="UTF-8") as fd:
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