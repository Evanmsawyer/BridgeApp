#Contains classes for the linparser.py script

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
        self.total_boards = self.endBoard - self.startBoard + 1
        self.boards = []
        board_count = 0
    
    def add_board(self, b):
        self.boards.append(b)

class Board:
    """Object representing one board of a round in a Bridge tournament"""
    pos_dic = {
        1 : "S",
        2 : "W",
        3 : "N",
        4 : "E"
    }
    def add_hands(self, hand_data):
        hand_list = hand_data.split(',')
        self.hands = []
        pos = 0
        for hand in hand_list:
            self.hands.append(Hand(self.pos_dic[pos], hand))
            pos += 1

    def __init__(self, board_num, bid_info, tricks):
        self.board_num = board_num
        bid_info = bid_info.split('|')
        #get dealer position
        if 1 <= bid_info[5][0] <= 4:
            self.dealer = self.pos_dic[bid_info[5][0]]
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
        self.tables.append(Table(bid_info, tricks))
        
    



class Table:
    """Object representing one table of one board of a Bridge tournament"""
    pass

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

    def __init__(self, pos, data):
        self.position = pos
        #split hand by suit
        data = data.translate(self.trans_table)
        suit_list = data.split(',')
        #hand info always goes spades -> hearts -> diamonds -> clubs
        pass

class Bid:
    """Object representing the bidding phase at a table"""
    pass