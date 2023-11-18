from bisect import bisect
#Contains classes for the linparser.py script
#global dictionary for dealer position
pos_dic = {
   -1 : "",
    1 : "S",
    2 : "W",
    3 : "N",
    4 : "E"
}
#tables used for calculating negative raw scores/international matchpoints
not_vul_scores = (
    (50, 100, 200), (100, 300, 600), (150, 500, 1000), (200, 800, 1600),
    (250, 1100, 2200), (300, 1400, 2800), (350, 1700, 3400), (400, 2000, 4000),
    (450, 2300, 4600), (500, 2600, 5200), (550, 2900, 5500), (600, 3200, 6400), 
    (650, 3500, 7000))
vul_scores = (
    (100, 200, 400), (200, 500, 1000), (300, 800, 1600), (400, 1100, 2200),
    (500, 1400, 2800), (600, 1700, 3400), (700, 2000, 4000), (800, 2300, 4600),
    (900, 2600, 5200), (1000, 2900, 5800), (1100, 3200, 6400), (1200, 3500, 7000), 
    (1300, 3800, 7600))
imp_calc = (0,20,40,80,120,160,210,260,310,360,420,490,590,740,890,1090,1290,1490,1740,1990,2240,2490,2990,3490,3990,15200)

class Round:
    """Object representing a round of a Bridge tournament"""
    def score_round(self):
        team1 = self.teams[0]
        team2 = self.teams[1]
        team1.endScore = team1.startScore
        team2.endScore = team1.startScore
        for b in self.boards:
            if b.team1_imps > 0:    team1.endScore += b.team1_imps
            else:                   team2.endScore += b.team2_imps

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
        self.player_list = playerList
        #build player list for teams
        team_list = [playerList[0], playerList[2], playerList[5], playerList[7]]
        self.teams.append(Team(headerParts[5], headerParts[6], team_list))
        team_list = [playerList[1], playerList[3], playerList[4], playerList[6]]
        self.teams.append(Team(headerParts[7], headerParts[8], team_list))
        #initialize board array
        self.total_boards = self.endBoard - self.startBoard + 1
        self.boards = []
        self.board_count = 0
    
    def __str__(self):
        res = '\"' + self.tournament_name + '\",\"' + self.teams[0].team_name + '\",\"' + self.teams[1].team_name + '\"'
        return res

class Board:
    """Object representing one board of a round in a Bridge tournament"""
    def score_board(self):
        table1 = self.tables[0]
        table2 = self.tables[1]
        team1_raw = table1.score if table1.declarer % 2 == 1 else -table1.score
        team2_raw = table2.score if table2.declarer % 2 == 1 else -table2.score
        imp_score = bisect(imp_calc, abs(team1_raw - team2_raw))
        self.team1_imps = imp_score if team1_raw > team2_raw else -imp_score
        self.team2_imps = -self.team1_imps

    def add_table(self, bid_info, tricks):
        bid_info = bid_info.split('|')
        self.tables.append(Table(self.dealer, bid_info, tricks, self.vuln))

    def add_hands(self, hand_data):
        hand_list = hand_data.split(',')
        self.hands = []
        pos = 1
        for hand in hand_list:
            self.hands.append(Hand(pos, hand))
            pos += 1

    def __init__(self, board_num, bid_info, tricks):
        self.board_num = board_num
        bid_info = bid_info.split('|')
        #get dealer position
        i = bid_info.index("md")
        if 1 <= int(bid_info[i + 1][0]) <= 4:
            self.dealer = int(bid_info[i + 1][0])
        else:
            self.dealer = -1
        #get vulnerability
        j = bid_info.index("sv")
        #o = none, n = N/S vulnerability, e = E/W vulnerability, b = both N/S and E/W vulnerability
        match bid_info[j + 1]:
            case "o" | "n" | "e" | "b":
                self.vuln = bid_info[j + 1].upper()
            case "0":
                self.vuln = "O"
            case _:
                self.vuln = ""
        #init table list and add hands
        self.add_hands(bid_info[i + 1][1:])
        self.tables = []
        self.tables.append(Table(self.dealer, bid_info, tricks, self.vuln))
    
    def __str__(self):
        sep = '\",\"'
        res = '\"' + pos_dic[self.dealer] + sep + self.vuln + '\",' + str(self.team1_imps) + ',' + str(self.team2_imps)
        return res

class Table:
    """Object representing one table of one board of a Bridge tournament"""
    def count_tricks(self):
        self.tricks_taken = 0
        for t in self.tricks:
            #if two positions are on the same team, they are either both even (E/W) or both odd (N/S)
            if self.declarer % 2 == t.winner % 2:
                self.tricks_taken += 1

    def add_tricks(self, trick_data):
        has_claim = False
        leader = self.declarer
        self.tricks = []
        trick_str = ""
        for s in trick_data: trick_str += s
        trick_str = trick_str.split('\n')
        #read through tricks
        for line in trick_str:
            if "mc" not in line and "pc" in line:
                if len(self.tricks) > 0:
                    leader = self.tricks[-1].winner
                self.tricks.append(Trick(leader, self.suit, len(self.tricks) + 1, line))
            elif "mc" in line:
                has_claim = True
                claim_trick = line.split('|')
        if has_claim:
            self.tricks_taken = int(claim_trick[-4])
        else:
            self.count_tricks()

    def get_declarer(self):
        for b in self.bids:
            if b.suit == self.suit and b.declarer % 2 == self.last_bid.declarer % 2:
                return b.declarer

    def get_score(self):
        contract_diff = self.tricks_taken - (self.contract_level + 6)
        #set score table
        match self.vuln:
            case "O": score_table = not_vul_scores
            case "B": score_table = vul_scores
            case "N": score_table = vul_scores if self.declarer % 2 == 1 else not_vul_scores
            case "E": score_table = vul_scores if self.declarer % 2 == 0 else not_vul_scores
        is_vuln = score_table is vul_scores
        #if contract was made
        if contract_diff >= 0:
            #calculate booleans
            minors = self.suit == 'C' or self.suit == 'D'
            majors = self.suit == 'H' or self.suit == 'S'
            nt = not majors and not minors
            game = (minors and self.contract_level >= 5) or (majors and self.contract_level >= 4) or (nt and self.contract_level >= 3)
            grand_slam = self.contract_level >= 7
            small_slam = self.contract_level >= 6 and not grand_slam

            #calculate suit bonuses
            if majors:      trick_score = self.contract_level * 30
            elif minors:    trick_score = self.contract_level * 20
            else:           trick_score = self.contract_level * 40
            #calculate over-bid bonuses
            match self.status:
                case 0:
                    trick_score += contract_diff * 20 if minors else contract_diff * 30
                    double_bonus = 0
                case 1:
                    trick_score += contract_diff * 200 if is_vuln else contract_diff * 100
                    double_bonus = 100 if is_vuln else 50
                case 2:
                    trick_score += contract_diff * 400 if is_vuln else contract_diff * 200
                    double_bonus = 100 if is_vuln else 50
            #calculate game bonus
            if game:            game_bonus = 500 if is_vuln else 300
            else:               game_bonus = 50
            #calculate slam bonuses
            if grand_slam:      slam_bonus = 1500 if is_vuln else 1000
            elif small_slam:    slam_bonus = 750 if is_vuln else 500
            else:               slam_bonus = 0

            self.score = trick_score + double_bonus + game_bonus + slam_bonus
        #if contract was failed
        else:
            contract_diff = -contract_diff
            self.score = -score_table[contract_diff - 1][self.status]

    def __init__(self, dealer, bid_info, tricks, vuln):
        self.vuln = vuln
        #set room
        match bid_info[1][0]:
            case 'o' | 'c': self.room = bid_info[1][0].upper()
            case _: self.room = ""
        i = bid_info.index("mb")
        bid_info = bid_info[i + 1:]
        #recombine bid info for easier splitting
        bid_str = ""
        for token in bid_info:
            bid_str = bid_str + token
        #split into separate bids
        bid_lst = bid_str.split("mb")
        #construct Bid objects
        self.bids = []
        bidding_opened = False
        for b in bid_lst:
            bid = Bid(dealer, b)
            self.bids.append(bid)
            dealer += 1
            if dealer > 4:
                dealer = 1
            if (not bid.is_pass) and not bidding_opened:
                self.first_bid = bid
                bidding_opened = True
            if (not bid.is_pass) and bid.doubled == 0:
                self.last_bid = bid
        #store important bid info
        self.status = self.bids[-4].doubled
        self.suit = self.last_bid.suit
        self.declarer = self.get_declarer()
        self.contract_level = self.last_bid.value
        self.result = str(self.contract_level) + self.suit
        self.add_tricks(tricks)
        #store results of table
        if self.tricks_taken == self.contract_level + 6:
            self.result = self.result + "="
        elif self.tricks_taken > self.contract_level + 6:
            self.result = self.result + "+" + str(self.tricks_taken - (self.contract_level + 6))
        else:
            self.result = self.result + "-" + str((self.contract_level + 6) - self.tricks_taken)
        self.get_score()

    def __str__(self):
        sep = '\",\"'
        res = '\"'
        for b in self.bids:
            res += str(b) + ','
        res = res[0:-1]
        res += sep + str(self.first_bid) + sep + str(self.last_bid) + sep + self.result + '\",' + str(self.score)
        return res

class Trick:
    """Object representing one trick at one table of a Bridge tournament"""
    #lookup for card ranks (aces high)
    rank_lst = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    def __str__(self):
        sep = '\",\"'
        res = '\"' + pos_dic[self.leader] + sep + pos_dic[self.winner] + sep
        for card in self.cards:
            res += card
        res += '\"'
        return res

    def __init__(self, leader, trump_suit, num, play):
        self.leader = leader
        self.num = num
        max_lead = -1
        max_trump = -1
        #clean play string
        play = play.replace("pc", "").replace("pg", "").replace("|", "")
        #split into individual cards
        self.cards = [play[i:i + 2].upper() for i in range(0, 8, 2)]
        curr_pos = leader
        #loop through cards to determine winner
        for card in self.cards:
            suit = card[0]
            val = Trick.rank_lst.index(card[1])
            if curr_pos == leader:
                lead_suit = suit
            if max_trump == -1 and suit == lead_suit and val > max_lead:
                max_lead = val
                self.winner = curr_pos
            if trump_suit != 'N' and suit == trump_suit and val > max_trump:
                max_trump = val
                self.winner = curr_pos
            curr_pos = (curr_pos % 4) + 1

class Team:
    """Object representing a team participating in a Bridge tournament"""

    def __str__(self):
        return '\"' + self.team_name + '\"'

    def __init__(self, name, startScore, member_list):
        self.team_name = name
        self.startScore = int(startScore)
        self.endScore = int(startScore)
        self.members = member_list

class Hand:
    """Object representing one hand of a board at a Bridge tournament"""
    trans_table = str.maketrans("HDC", ",,,")

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
        data = data[1:].translate(self.trans_table)
        self.suits = data.split(',')
        #get suit distribution and hcp
        self.dist = ""
        for suit in self.suits:
            self.dist += str(len(suit))
        self.get_hcp()
    
    def __str__(self):
        sep = '\",\"'
        res = ('\"' + pos_dic[self.position] + sep + self.suits[0] + sep + self.suits[1] + 
               sep + self.suits[2] + sep + self.suits[3] + '\",' + str(self.hcp) + ',\"' + str(self.dist) + '\"')
        return res

class Bid:
    """Object representing a bid at a table"""
    def __str__(self):
        res = pos_dic[self.declarer] + ':'
        if self.is_pass:
            res += "P"
            return res
        match self.doubled:
            case 0:
                res += str(self.value) + self.suit
            case 1:
                res += "X"
            case 2:
                res += "XX"
        return res

    def __init__(self, dealer, info):
        self.declarer = dealer
        split_info = info.partition("an")
        token = split_info[0]
        #check if alerted
        if '!' in token: self.alerted = True
        else: self.alerted = False
        #parse bid and check for pass/double/redouble
        self.value = 0
        self.suit = None
        self.is_pass = False
        self.doubled = 0
        match token[0]:
            case 'p': self.is_pass = True
            case 'd': self.doubled = 1
            case 'r': self.doubled = 2
            case _:
                self.value = int(token[0])
                self.suit = token[1].upper()
                self.doubled = 0
        #add comment if provided
        if len(split_info[2]) > 0:
            self.comment = split_info[2]
        else:
            self.comment = None