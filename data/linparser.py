#Parser for converting .lin files into .csv files
import glob
import sys
import os
import parser_classes
#FLOW OF LOGIC

if len(sys.argv) != 2:
    print("Usage: py linparser.py <directory>\n")
    exit()

def readFile(filename):
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
            curr_line = fd.readline()
            while not curr_line.startswith("qx"):
                tricks.append(curr_line)
                curr_line = fd.readline()

            board = parser_classes.Board(board_num, bid_phase, tricks)


#Create match object
    #store tournament info
    #store segment info
    #store scoring type
    #store start and end board numbers
    #create team objects (team name, members, starting score)
    #calculate total board count for match
#for each board in match:
    #read bid info from file
    #read tricks from file
    #create board object (has dealer, vulnerability, hand info, suit holding, high card points, bid info, trick info)
    #parse play 1
    #parse play 2
    #calculate scoring of board (if IMP scoring)
#calculate score of match overall
#print to csv file(s)