#Parser for converting .lin files into .csv files
import glob
import sys
import os
import parser_classes
import json

r_id = 0; b_id = 0; h_id = 0; t_id = 0
if os.path.isfile("parser_config.json"):
    with open("parser_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    config = config["parser"]
    r_id = config["r_id"]
    b_id = config["b_id"]
    h_id = config["h_id"]
    t_id = config["t_id"]

def read_file(filename):
    if not (os.path.isfile(filename)):
        return
    #open file
    with open(filename, mode='r', encoding='utf-8') as fd:
        #read header
        header = fd.readline()
        #split header
        headerParts = header[3:].strip('|').split(sep=',')
        #read results
        res = fd.readline()
        #read players
        player_raw = fd.readline()
        player_list = player_raw.split(sep='|')[1].split(sep=',')

        #create round object
        round = parser_classes.Round(headerParts, player_list)
        board_num = round.startBoard
        curr_line = fd.readline()
        bid_phase = curr_line
        while round.board_count < round.total_boards:
            tricks = []
            #load first table & create board
            curr_line = fd.readline()
            while not curr_line.startswith("qx"):
                tricks.append(curr_line)
                curr_line = fd.readline()

            curr_board = parser_classes.Board(board_num, bid_phase, tricks)
            board_num += 1
            
            #load second table into board
            bid_phase = curr_line
            tricks.clear()
            curr_line = fd.readline()
            while len(curr_line) > 0 and not curr_line.startswith("qx"):
                tricks.append(curr_line)
                curr_line = fd.readline()
            curr_board.add_table(bid_phase, tricks)
            bid_phase = curr_line
            tricks.clear
            curr_board.score_board()
        round.score_round()
        return round

def q(x):
    return "\"" + str(x) + "\""

def write_csv(round: parser_classes.Round):
    #open files
    with (open("round.csv", "a", encoding="UTF-8") as round_csv, open("board.csv", "a", encoding="UTF-8") as board_csv,
          open("table.csv", "a", encoding="UTF-8") as table_csv, open("hand.csv", "a", encoding="UTF-8") as hand_csv,
          open("trick.csv", "a", encoding="UTF-8") as trick_csv, open("team.csv", "a", encoding="UTF-8") as team_csv,
          open("player.csv", "a", encoding="UTF-8") as player_csv, open("plays_table.csv", "a", encoding="UTF-8") as p_t_csv):
        #write to round.csv (round_id, tournament_name, team_one_name, team_two_name)
        print(r_id, round, file=round_csv, sep=",")

        #write to board.csv (board_id, round_id, dealer, vuln)
        for board in round.boards:
            print(b_id, r_id, board, file=board_csv, sep=",")
            #write to hand.csv (hand_id, board_id, position, spades, hearts, diamonds, clubs, hcp)
            for hand in board.hands:
                print(h_id, b_id, hand, file=hand_csv, sep=",")
                h_id += 1

            #write to table.csv (table_id, board_id, paired_id, bid_phase, last_bid, result, declarer_score)
            table_1 = board.tables[0]
            table_2 = board.tables[1]
            print(t_id, (t_id + 1), b_id, table_1, file=table_csv, sep=",")
            print((t_id + 1), t_id, b_id, table_2, file=table_csv, sep=",")

            #write to trick (num, t_id, play, start_pos)
            for trick in table_1.tricks:
                print(q(trick.num), t_id, trick, file=trick_csv, sep=",")
            for trick in table_2.tricks:
                print(q(trick.num), (t_id + 1), trick, file=trick_csv, sep=",")
            
        #write to team.csv
        for team in round.teams:
            print(team, file=team_csv)
            #write to player.csv
            for player in team.members:
                p_string = '\"' + player + '\"'
                print(p_string + team, sep=',', file=player_csv)

    #RELATIONSHIPS
    #write to Plays_table

def main():
    round_lst = None
    #read files in and write to CSVs
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if os.path.isdir(arg):
                for f in glob.iglob(arg + "*.lin"):
                    round = read_file(f)
                    write_csv(round)
            elif os.path.isfile(arg):
                round = read_file(arg)
                write_csv(round)
    else:
        for f in glob.iglob("*.lin"):
            round = read_file(f)
            write_csv(round)
    #remove duplicates from CSVs

def __init__():
    main()