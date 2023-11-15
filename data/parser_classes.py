#Contains classes for the linparser.py script

#global dictionary for dealer position
pos_dic = {
    1 : "S",
    2 : "W",
    3 : "N",
    4 : "E"
}

class Round:
    """Object representing a round of a Bridge tournament"""
    def __init__(self, headerParts, playerList):
        self.tournament_name = headerParts[0]
        self.segment = headerParts[1]
        if headerParts[2] == "I":
            self.scoreType = "IMPS"
        else:
            self.scoreType = None
        self.startBoard = int(headerParts[3])
        self.endBoard = int(headerParts[4])
        self.teams = []
        #build player list for teams
        team_list = [playerList[0], playerList[2], playerList[5], playerList[7]]
        self.teams.append(Team(headerParts[5], headerParts[6], team_list))
        team_list = playerList - team_list
        self.teams.append(Team(headerParts[7], headerParts[8], team_list))
        #initialize board array
        self.total_boards = self.endBoard - self.startBoard + 1
        self.boards = []
        self.board_count = 0
    
    def add_board(self, b):
        self.boards.append(b)

class Board:
    """Object representing one board of a round in a Bridge tournament"""
    
    def add_hands(self, hand_data):
        hand_list = hand_data.split(',')
        self.hands = []
        pos = 0
        for hand in hand_list:
            self.hands.append(Hand(pos_dic[pos], hand))
            pos += 1

    def __init__(self, board_num, bid_info, tricks):
        self.board_num = board_num
        bid_info = bid_info.split('|')
        #get dealer position
        if 1 <= bid_info[5][0] <= 4:
            self.dealer = bid_info[5][0]
        else:
            self.dealer = None
        #get vulnerability
        #o = none, n = N/S vulnerability, e = E/W vulnerability, b = both N/S and E/W vulnerability
        match bid_info[7]:
            case "o" | "n" | "e" | "b":
                self.vuln = bid_info[7].upper()
            case _:
                self.vuln = None
        #init table list and add hands
        self.add_hands(bid_info[5][1:])
        self.tables = []
        self.tables.append(Table(self.dealer, bid_info, tricks))

class Table:
    """Object representing one table of one board of a Bridge tournament"""
    def __init__(self, dealer, bid_info, tricks):
        #set room
        match bid_info[1][0]:
            case 'o' | 'c': self.room = bid_info[1][0].upper()
            case _: self.room = None
        bid_info = bid_info[8:]
        #recombine bid info for easier splitting
        bid_str = ""
        for token in bid_info:
            bid_str = bid_str + token
        #split into separate bids
        bid_lst = bid_str.split("mb")
        #construct Bid objects
        self.bids = []
        for b in bid_lst:
            #add bid to list
            self.bids.append(Bid(dealer, b))
            #increment dealer
            dealer += 1
            if dealer > 4:
                dealer = 1
        #store final non-pass bid
        self.final_bid = self.bids[-4]



class Trick:
    """Object representing one trick at one table of a Bridge tournament"""
    pass

class Team:
    """Object representing a team participating in a Bridge tournament"""
    def __init__(self, name, startScore, member_list):
        self.teamName = name
        self.startScore = startScore
        self.members = member_list

class Hand:
    """Object representing one hand of a board at a Bridge tournament"""
    trans_table = str.translate("SHDC", ",,,,")

    def get_hcp(self):
        #calculate high card points for hand
        self.hcp = 0
        for suit in self.suits:
            for card in suit:
                match card:
                    case 'A': self.hcp += 4
                    case 'K': self.hcp += 3
                    case 'Q': self.hcp += 2
                    case 'J': self.hcp += 1

    def __init__(self, pos, data):
        self.position = pos
        #split hand by suit
        #suit order is always spades -> hearts -> diamonds -> clubs
        data = data.translate(self.trans_table)
        self.suits = data.split(',')
        #get suit distribution
        self.get_hcp()

class Bid:
    """Object representing a bid at a table"""
    def __init__(self, dealer, info):
        self.dealer = dealer
        split_info = info.partition("an")
        token = split_info[0]
        #check if alerted
        if token.find('!') >= 0: self.alerted = True
        else: self.alerted = False
        #CONTINUE HERE
