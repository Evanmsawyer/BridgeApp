#Parser for converting .lin files into .csv files
import glob
import sys
import os
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
        header = fd.readline
    
#Split header into parts (sep=',')
#Read results (2nd line)
#Read players (3rd line)
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