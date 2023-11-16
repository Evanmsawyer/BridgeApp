#Parser for converting .lin files into .csv files
import glob
import sys
import os
import parser_classes
import json

r_id = 0; b_id = 0; h_id = 0
if os.path.isfile("parser_config.json"):
    with open("parser_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    config = config["parser"]
    r_id = config["r_id"]
    b_id = config["b_id"]
    h_id = config["h_id"]

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
        print(q(r_id), q(round.tournament_name), q(round.teams[0].team_name), q(round.teams[1].team_name),
              file=round_csv)
        #write to board.csv (board_id, round_id, dealer, vuln)
        for board in round.boards:
            print(q(b_id), q(r_id), q(board.dealer), q(board.vuln), file=board_csv)
            #write to hand(hand_id, round_id, position, spades, hearts, diamonds, clubs, hcp)
            for hand in board.hands:
                print(q(h_id), q(b_id), q(hand.pos), q(hand.suits[0]), q(hand.suits[1]), q(hand.suits[2]), q(hand.suit[3]),
                      q(hand.hcp), file=hand_csv)
                h_id += 1
            #write to table.csv ()
    
    #write to table
    #write to trick
    #write to team  
    #write to player

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