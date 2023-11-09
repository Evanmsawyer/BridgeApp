#Parser for converting .lin files into .csv files

#FLOW OF LOGIC
#Open file
#Read header (1st line)
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