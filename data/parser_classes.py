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
    def __init__(self, board_num, bid_info, tricks):
        self.board_num = board_num
        

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
    pass

class Bid:
    """Object representing the bidding phase at a table"""
    pass