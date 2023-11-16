#Parser for converting .lin files into .csv files
import glob
import sys
import os
import parser_classes
#FLOW OF LOGIC

if len(sys.argv) != 2:
    print("Usage: py linparser.py <directory>\n")
    exit()

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

def write_csv(round):
    pass

def main():
    round_lst = None
    #read files in
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
    #write to csv files

def __init__():
    main()