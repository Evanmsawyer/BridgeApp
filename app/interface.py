import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk
import os
import json
from dbCommunicator import DBConnector
import enum
import sys
import os

current_script_directory = os.path.dirname(__file__)
adjacent_directory_path = os.path.join(current_script_directory, '..', 'data')
sys.path.insert(0, adjacent_directory_path)
import linparser

db = DBConnector()
result_tree = None
root = None
tab_search = None
tab_play_by_play = None
currentTable = None
currentNHand = None
currentSHand = None
currentEHand = None
currentWHand = None
currentTricks = None

class SelectCriteria(enum.Enum):
    Player = "Player"
    HCP = "HCP"
    FirstBid = "First Bid"
    LastBid = "Last Bid"
    BoardID = "Board Search"
    Tournament = "Tournament"
    Tricks = "Tricks"
    Slams = "Slams"
    PlayersByTeam = "Players By Team"
    Seat = "Seat"
    Dealer = "Dealer"
    Score = "Score"

    @property
    def description(self):
        descriptions = {
            SelectCriteria.Player: "Player (Name)",
            SelectCriteria.HCP: "HCP (High, Low)",
            SelectCriteria.FirstBid: "First Bid (OpeningBid)",
            SelectCriteria.LastBid: "Last Bid (EndingBid)",
            SelectCriteria.BoardID: "Board Search (BoardID)",
            SelectCriteria.Tournament: "Tournament (Name)",
            SelectCriteria.Tricks: "Tricks (TableID)",
            SelectCriteria.Slams: "Slams (N/A)",
            SelectCriteria.PlayersByTeam: "Players By Team (Team Name)",
            SelectCriteria.Seat: "Seat (TableID, Player Name, Team Name)",
            SelectCriteria.Dealer: "Dealer (Number)",
            SelectCriteria.Score: "Score (Low, High)",
        }
        return descriptions[self]
    
    @property
    def procedure(self):
        procedures = {
            SelectCriteria.Player: "PlayerSearch",
            SelectCriteria.HCP: "HCPSearchInRange",
            SelectCriteria.FirstBid: "OpeningBidSearch",
            SelectCriteria.LastBid: "EndingBidSearch",
            SelectCriteria.BoardID: "BoardSearch",
            SelectCriteria.Tournament: "TableInTournament",
            SelectCriteria.Tricks: "TotalTricksByPlayer",
            SelectCriteria.Slams: "SlamBidAndMade",
            SelectCriteria.PlayersByTeam: "PlayerSearchByTeam",
            SelectCriteria.Seat: "GetSeat",
            SelectCriteria.Dealer: "DealerSearch",
            SelectCriteria.Score: "RawScoreSearch",
        }
        return procedures[self]

# Function to update the result view
def update_result_view(columns, data):
    result_tree.delete(*result_tree.get_children())
    result_tree["columns"] = ()

    result_tree["columns"] = columns
    for col in columns:
        result_tree.heading(col, text=col)
        result_tree.column(col, width=120, minwidth=120, anchor="w")
    for row in data:
        row_values = [row[col] for col in columns]
        result_tree.insert('', 'end', values=row_values)

# Create a scrollable frame
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


# Function to add criteria to the search bar
def add_to_search():
    criteria = criteria_combobox.get().split(' (')[0]
    value = criteria_value_entry.get()
    existing_text = search_bar.get()
    new_search_text = f'{existing_text} "{criteria}:{value}"' if existing_text else f'"{criteria}:{value}"'
    search_bar.delete(0, tk.END)
    search_bar.insert(0, new_search_text)

# Function to execute the search
def execute_search():
    search_text = search_bar.get()
    for search in search_text.split('"'):
        if ':' in search:
            procedure_name, parameters = search.replace('"', '').split(':', 1)  # Removing quotes and splitting on the first colon
            parameters = tuple(parameters.split(','))
            
            print(f"Procedure: {procedure_name}, Parameters: {parameters}")
            if procedure_name == SelectCriteria.Tournament.value: 
                #Test Data: 2013 USBC USA2 Final
                procedure_name = SelectCriteria.Tournament.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.Tricks.value:
                #Test Data: 
                procedure_name = SelectCriteria.Tricks.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.HCP.value:
                procedure_name = SelectCriteria.HCP.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.LastBid.value:
                procedure_name = SelectCriteria.LastBid.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.BoardID.value:
                procedure_name = SelectCriteria.BoardID.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.Player.value:
                procedure_name = SelectCriteria.Player.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.Dealer.value:
                procedure_name = SelectCriteria.Dealer.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.PlayersByTeam.value:
                procedure_name = SelectCriteria.PlayersByTeam.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.Seat.value: 
                procedure_name = SelectCriteria.Seat.procedure 
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.Score.value:
                procedure_name = SelectCriteria.Score.procedure
                columns, data = db.execute_stored_procedure(procedure_name, parameters)
                update_result_view(columns, data)
            elif procedure_name == SelectCriteria.Slams.value: 
                procedure_name = SelectCriteria.Slams.procedure
                columns, data = db.execute_stored_procedure_with_no_parameters(procedure_name)
                update_result_view(columns, data)
            else:
                print("Invalid procedure name:", procedure_name)
        else:
            if search != '':
                print("Invalid format in search text:", search)

# Setting up the main window
root = tk.Tk()
root.title("Bridge Game Database Manager")
root.geometry("800x600")
root.maxsize(800, 600)

# Styling
style = ttk.Style()
style.theme_use('clam')

# Define colors
primary_color = '#2F4F4F'  
secondary_color = '#4682B4'  
text_color = '#F8F8FF'  # White
entry_background = '#D3D3D3'  # Slightly lighter blue-grey

# Background color
style.configure('TFrame', background=primary_color)
style.configure('TLabel', background=primary_color, foreground=text_color)
style.configure('TButton', background=secondary_color, foreground=text_color)

# Entry and Combobox styling
style.map('TEntry', fieldbackground=[('readonly', entry_background)])
style.map('TCombobox', fieldbackground=[('readonly', entry_background)])
#style.configure('TEntry', foreground=text_color, background=entry_background)
#style.configure('TCombobox', foreground=text_color, background=entry_background)

custom_font = ('Helvetica', 12)

# Main frame for tabs
main_frame = ttk.Frame(root,style='TFrame')
main_frame.pack(fill='both', expand=True)

# Using ttk.Notebook for tabbed views
notebook = ttk.Notebook(main_frame)  # Changed parent to main_frame
notebook.pack(expand=True, fill="both")

# Tab 1: Search and Results
tab_search = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_search, text="Search")

# Frame for search input widgets
search_input_frame = ttk.Frame(tab_search, padding="10", style='TFrame')
search_input_frame.pack(fill='x', expand=False, pady=15)

# Dropdown menu for criteria
criteria_label = ttk.Label(search_input_frame, text="Select Criteria:", font=custom_font, style='TLabel')
criteria_label.pack(side='left', padx=5, pady=5)

criteria_options = [c.description for c in SelectCriteria]

criteria_options.sort()
criteria_combobox = ttk.Combobox(search_input_frame, values=criteria_options, state='readonly', font=custom_font)
criteria_combobox.pack(side='left', padx=criteria_options.__len__(), pady=criteria_options.__len__())

criteria_value_entry = ttk.Entry(search_input_frame, font=custom_font)
criteria_value_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

add_button = ttk.Button(search_input_frame, text="Add to Search", command=add_to_search, style='TButton')
add_button.pack(side='left', padx=5, pady=5)

# Search bar and button
search_bar_frame = ttk.Frame(tab_search, padding="10", style='TFrame')
search_bar_frame.pack(fill='x', expand=False)

search_bar = ttk.Entry(search_bar_frame, font=custom_font)
search_bar.pack(side='left', fill='x', expand=True, padx=5, pady=5)

search_button = ttk.Button(search_bar_frame, text="Search", command=execute_search, style='TButton')
search_button.pack(side='left', padx=5, pady=5)

# Scrollable frame for search results
#scroll_frame = ScrollableFrame(tab_search)
#scroll_frame.pack(fill='both', expand=True)

# Configure the Treeview inside the scrollable frame for results
result_tree = ttk.Treeview(tab_search, show="headings")
result_tree.pack(side="bottom", padx="5", pady="5", fill="both", expand=True)

scrollbar_horizontal = ttk.Scrollbar(tab_search, orient="horizontal", command=result_tree.xview)
scrollbar_horizontal.pack(side="bottom", fill="x")
result_tree.configure(xscrollcommand=scrollbar_horizontal.set)

def on_tree_selection(event):
    selected_items = result_tree.selection()
    columns = result_tree.cget("columns")
    if selected_items:  # Check if something is selected
        item = result_tree.item(selected_items[0])  # Assuming single selection
        row_data = item['values']
  
        # Assuming 'TableID' is one of the columns, and we know its index
        # Replace 'table_id_index' with the actual index of 'TableID' column
        if "TableID" in columns:
            table_id_index = columns.index('TableID')
            table_id = row_data[table_id_index]
            print(f"Selected TableID: {table_id}")  # Or perform other actions with the TableID
            currentTable = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
            currentNHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (3, table_id))
            currentSHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (1, table_id))
            currentEHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (4, table_id))
            currentWHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (2, table_id))
            currentTricks = db.execute_query("SELECT * FROM Trick WHERE Trick.TableID = %s ORDER BY Trick.TrickNumber ASC"% (table_id,))
            bridge_app = BridgeGameApp(currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks)
            update_statistics_view(currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks)
        
        if "PlayerName" or "TeamName" in columns:
            PlayerName_index = columns.index('Name')
            PlayerName_id = row_data[PlayerName_index]
            TeamName_index = columns.index('TeamName')
            TeamName_id = row_data[TeamName_index]
            print(f"Selected TableID: {PlayerName_id} on team {TeamName_id}")  # Or perform other actions with the TableID
            

result_tree.bind("<<TreeviewSelect>>", on_tree_selection)

#result_tree.heading("Column1", text="")
#result_tree.column("Column1", width=120)


# Tab 2: Play-by-Play Details
tab_play_by_play = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_play_by_play, text="Play-by-Play")

script_dir = os.path.dirname(os.path.abspath(__file__))
cards_folder = 'assets/cards'
cards_path = os.path.join(script_dir, cards_folder)
pos_dic = {
    0 : "S",
    1 : "W",
    2 : "N",
    3 : "E"
}

class BridgeGameApp:      
    def __init__(self, currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks):
        for widget in tab_play_by_play.winfo_children():
            widget.destroy()
        self.currentTricks = currentTricks
        # Initialize game state
        self.current_play = 0
        self.tricks_north_south = 0
        self.tricks_east_west = 0
        last_bid = currentTable[0][5]

        # Define the font to use for card display
        self.card_font = tk.font.Font(family='Helvetica', size=16, weight='bold')

        # Create a container frame within the notebook tab
        self.container_frame = tk.Frame(tab_play_by_play, background='#2F4F4F')
        self.container_frame.pack(expand=True, fill=tk.BOTH)

        # Configure the container grid
        self.container_frame.grid_rowconfigure(1, weight=2)
        self.container_frame.grid_columnconfigure(1, weight=2)
        for i in [0, 2]:
            self.container_frame.grid_rowconfigure(i, weight=1)
            self.container_frame.grid_columnconfigure(i, weight=1)
        
        # Define the player frames
        self.north_frame = tk.Frame(self.container_frame, bg='light gray', width=200, height=200)
        self.east_frame = tk.Frame(self.container_frame, bg='light gray', width=100, height=200)
        self.south_frame = tk.Frame(self.container_frame, bg='light gray', width=200, height=200)
        self.west_frame = tk.Frame(self.container_frame, bg='light gray', width=100, height=200)
        self.center_frame = tk.Frame(self.container_frame, bg='white', width=200, height=200)

        # Initialize the Text widget for center cards
        self.center_label = tk.Label(self.center_frame, text='', font=self.card_font, bg='white')
        self.center_label.pack(expand=True, fill=tk.BOTH)

        self.player_frames = {
            0: self.north_frame,
            1: self.east_frame,
            2: self.south_frame,
            3: self.west_frame
        }
        
        # Prevent the frames from shrinking smaller than their contents
        for frame in [self.north_frame, self.east_frame, self.south_frame, self.west_frame, self.center_frame]:
            frame.grid_propagate(False)
        
        # Place the frames in the grid
        self.north_frame.grid(row=0, column=1, sticky='ew')
        self.east_frame.grid(row=1, column=2, sticky='ns')
        self.south_frame.grid(row=2, column=1, sticky='ew')
        self.west_frame.grid(row=1, column=0, sticky='ns')
        self.center_frame.grid(row=1, column=1, sticky='nsew')

        self.container_frame.grid_rowconfigure(0, weight=1, minsize=100)
        self.container_frame.grid_rowconfigure(1, weight=2, minsize=300)
        self.container_frame.grid_rowconfigure(2, weight=1, minsize=100)

        self.container_frame.grid_columnconfigure(0, weight=1, minsize=100)
        self.container_frame.grid_columnconfigure(1, weight=2, minsize=300)
        self.container_frame.grid_columnconfigure(2, weight=1, minsize=100)

        print(currentNHand[0])
        # Sample data
        self.hands = {
            0: currentNHand[0],
            1: currentEHand[0],
            2: currentSHand[0],
            3: currentWHand[0],
        }
        self.handsReverse = {
            0: ('', '',  '', '', ''),
            1: ('', '',  '', '', ''),
            2: ('', '',  '', '', ''),
            3: ('', '',  '', '', ''),
        }

        # Display initial hands
        self.display_hand(self.north_frame, self.hands[0], horizontal=True)
        self.display_hand(self.east_frame, self.hands[1], horizontal=False)
        self.display_hand(self.south_frame, self.hands[2], horizontal=True)
        self.display_hand(self.west_frame, self.hands[3], horizontal=False)

        # Placeholder for card labels (to display card images)
        self.center_cards = []

        # Initialize labels for the trick counters
        self.tricks_ns_label = tk.Label(self.container_frame, text='NS: 0', font=self.card_font, bg='light gray')
        self.tricks_ns_label.grid(row=0, column=0, sticky='nw')

        self.tricks_ew_label = tk.Label(self.container_frame, text='EW: 0', font=self.card_font, bg='light gray')
        self.tricks_ew_label.grid(row=0, column=2, sticky='ne')

        # Final Bid label
        final_bid_label = tk.Label(self.container_frame, text=f"Final bid: {last_bid}", font=self.card_font, bg='light gray')
        final_bid_label.grid(row=0, column=1, sticky='n')

        # Initialize or load a game state here
        self.center_label = tk.Label(self.center_frame, text='', font=self.card_font, bg='white')
        self.center_label.pack(expand=True, fill=tk.BOTH, anchor='center')

         # Add navigation buttons
        self.back_button = tk.Button(self.container_frame, text="Back", command=self.move_back)
        self.back_button.grid(row=3, column=0, sticky='ew')

        self.next_button = tk.Button(self.container_frame, text="Next", command=self.move_next)
        self.next_button.grid(row=3, column=2, sticky='ew')

        self.north_frame.pack_propagate(False)
        self.east_frame.pack_propagate(False)
        self.south_frame.pack_propagate(False)
        self.west_frame.pack_propagate(False)
        self.center_frame.pack_propagate(False)

        # Initialize the current play index
        self.current_play_index = 0

    def update_center(self, player_with_cards, cards_played, replace=False):
        # Add or remove cards from the center display based on the direction of the move
        #self.center_text.delete('1.0', tk.END)
        if len(player_with_cards) != 4:
            return
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        if replace:
            # Replace the center cards with the new set
            self.center_cards = list(cards_played)
        else:
            # If moving forward, add the new cards to the display
            self.center_cards.extend(cards_played)

        savedPos = {}
        # Update the center Label widget with the current cards
        for card in self.center_cards:
            # Find the player who played the card
           # print(card)
            #player_with_card = self.find_player_with_card(card)
            player_with_card=player_with_cards[card]

            # Create a label for the player and pack it
            player_label = tk.Label(self.center_frame, text=f"Player {player_with_card}", font=self.card_font, bg='white')
            player_label.pack()

            # Create a label for the card and pack it
            card_label = tk.Label(self.center_frame, text=card, font=self.card_font, bg='white')
            card_label.pack()


    def display_hand(self, frame, hand_tuple, horizontal=True):
    # Clear the frame first
        for widget in frame.winfo_children():
            widget.destroy()

        # Convert the hand tuple into a string with suit symbols
        suits = ['♠', '♥', '♦', '♣']
        hand_strings = [f"{suits[i]}{cards}" for i, cards in enumerate(hand_tuple[:4])]

        if horizontal:
            # For horizontal frames (North and South), use one label for each suit
            for suit_str in hand_strings:
                label = tk.Label(frame, text=suit_str, font=self.card_font, bg='light gray')
                label.pack(side=tk.LEFT, anchor='w', padx=5)
        else:
            frame.update_idletasks()

            # Use the updated frame dimensions for the canvas
            canvas_width = frame.winfo_width()
            canvas_height = frame.winfo_height()
            canvas = tk.Canvas(frame, bg='light gray', width=canvas_width, height=canvas_height)
            canvas.pack(side=tk.TOP, fill='both', expand=True)
            
            # Calculate the starting y position to center the suits vertically
            start_y = (canvas_height - (len(hand_strings) * 20)) // 2
            y_position = start_y
            for suit_str in hand_strings:
                canvas.create_text(canvas_width // 2, y_position, text=suit_str, font=self.card_font, anchor="center")
                y_position += 20  # Space between suits

    def update_hand(self, player, card_played, remove=False):
        print(player)
        player = int(player)
        hand_tuple = self.hands.get(player)
        hand_tuplerev = self.handsReverse.get(player)

        if hand_tuple is None:
            # Handle error: no hand found for this player number
            print(f"No hand found for player {player}")
            return
        
        hand_list = list(hand_tuple)
        hand_listrev = list(hand_tuplerev)
        # Debug print to check the card
        print(f"Card being updated: {card_played}")

        try:
            suit_index = 'SHDC'.index(card_played[0])
        except ValueError:
            print(f"Invalid card suit: {card_played[0]}")
            return  # Exit the method if the suit is not valid
        #print(hand_listrev)
        suit_hand = hand_list[suit_index]
        suit_hand_rev = hand_listrev[suit_index]
        if remove:
            # Moving backward: Add the card back to the player's main hand
            # and remove it from the reverse hand
            hand_list[suit_index] = suit_hand + card_played[1:]
            hand_listrev[suit_index] = suit_hand_rev.replace(card_played[1:], '', 1)
        else:
            # Moving forward: Remove the card from the player's main hand
            # and add it to the reverse hand
            hand_list[suit_index] = suit_hand.replace(card_played[1:], '', 1)
            hand_listrev[suit_index] = suit_hand_rev + card_played[1:]
        #print(hand_listrev)

        self.hands[player] = tuple(hand_list)
        self.handsReverse[player] = tuple(hand_listrev)
        #print(self.handsReverse[player])
        self.display_hand(self.player_frames[player], self.hands[player], horizontal=player in [0, 2])

    """
    def play_game(self, plays):
        # Loop through the plays and update hands accordingly
        for play in plays.values():
            player, cards_played = play[2], play[4]
            self.update_hand(player, [cards_played[i:i+2] for i in range(0, len(cards_played), 2)])"""

    def move_next(self):
        print(self.current_play_index)
        if self.current_play_index < len(self.currentTricks) - 1:
            self.current_play_index += 1
            self.play_current()
        else:
            self.end_label = tk.Label(self.center_frame, text="Rest of Tricks Claimed" , font=self.card_font, bg='white')
            self.end_label.pack()

    def move_back(self):
        print(self.current_play_index)
        if self.current_play_index > 1:
            self.current_play_index -= 1
            self.play_current(backward=True)

    def find_player_with_card(self, card, reverse=False):
        suit_order = {'S': 0, 'H': 1, 'D': 2, 'C': 3}
        handsRef = self.hands
        if reverse == True:
            handsRef = self.handsReverse
        for player, hand_tuple in handsRef.items():
            suit = card[0]  # The suit of the card ('S', 'H', 'D', 'C')
            value = card[1:]  # The value of the card ('6', 'A', 'Q', etc.)

            suit_index = suit_order.get(suit)  # Get the index of the suit in the tuple
            if suit_index is not None and value in hand_tuple[suit_index]:
                return player
        return None  # Return None if the card is not found in any hand

    def play_current(self, backward=False):
        # Retrieve the current play
        current_play = self.currentTricks[self.current_play_index]

        cards_played = current_play[4]
        
        # Extract information from the current play
        trick_number, table_id, first_seat, winning_seat, cards_played = current_play

        # Split the cards_played string into individual cardsself.hands
        cards = [cards_played[i:i+2] for i in range(0, len(cards_played), 2)]

        savedPos={}
        if backward:
            # If moving backward, remove the last played cards from the display
            # and add them back to each player's hand
            for card in cards:
                print(card)
                #self.update_center(None, cards, replace=True)
                player_with_card = self.find_player_with_card(card, True) 
                print(player_with_card)
                savedPos[card] = pos_dic[player_with_card]

                if player_with_card is not None:
                    self.update_hand(player_with_card, card, remove=True)
                    self.update_center(savedPos, cards, replace=True)
            # Decrement the trick counter for the team that won this trick
            self.update_trick_counters(winning_seat, decrement=True)
        else:
            # If moving forward, remove each card from the respective player's hand
            # and replace the cards in the center
            for card in cards:
                #self.update_center(None, cards, replace=True)
                player_with_card = self.find_player_with_card(card) 
                savedPos[card] = pos_dic[player_with_card]

                if player_with_card is not None:
                    self.update_hand(player_with_card, card)
                    self.update_center(savedPos, cards, replace=True)
            # Increment the trick counter for the team that won this trick
            self.update_trick_counters(winning_seat, decrement=False)

    def update_trick_counters(self, winning_seat, decrement=False):
        # Determine the team that won the trick
        if winning_seat in [1, 3]:  # North or South
            if decrement:
                self.tricks_north_south = max(0, self.tricks_north_south - 1)
            else:
                self.tricks_north_south += 1
            self.tricks_ns_label.config(text=f'NS: {self.tricks_north_south}')
        elif winning_seat in [2, 4]:  # East or West
            if decrement:
                self.tricks_east_west = max(0, self.tricks_east_west - 1)
            else:
                self.tricks_east_west += 1
            self.tricks_ew_label.config(text=f'EW: {self.tricks_east_west}')


# Tab 3: Statistics Details
tab_statistics = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_statistics, text="Statistics")

def fetch_statistics(currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks):
    table_id = currentTable[0][0]
    plays_table = db.execute_query(f"SELECT PlayerName, TeamName FROM PlaysTable WHERE TableID = {table_id}")

    # Dictionary to store statistics for each player
    player_stats = {}
    
    # Fetch statistics for each player
    for i in range(0, 4):
        team_name = list(plays_table[i])[0]
        player_name = list(plays_table[i])[1]
        key = f"{team_name}{player_name}"
        total_tricks = db.execute_query("SELECT COUNT(*) FROM (SELECT TableID, Seat FROM BridgeDB.PlaysTable WHERE PlayerName = '%s' AND TeamName = '%s' AND TableID = %s) AS T NATURAL JOIN BridgeDB.Trick WHERE T.Seat = WinningSeat;"%(player_name, team_name, table_id,))
        player_stats[f"{player_name} on team {team_name} has Total Tricks "] = total_tricks

    return player_stats
    #return {
        #"North Player Total Tricks": total_tricks,
    #}

# Function to update statistics view
def update_statistics_view(currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks):
    stats = fetch_statistics(currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks)

    for i, (stat_name, stat_value) in enumerate(stats.items()):
        ttk.Label(tab_statistics, text=f"{stat_name}:", style='TLabel').grid(row=i, column=0, sticky='W', padx=5, pady=5)
        ttk.Label(tab_statistics, text=str(stat_value), style='TLabel').grid(row=i, column=1, sticky='W', padx=5, pady=5)

# Tab 4: Edit
tab_edit = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_edit, text="Edit")

def update_player_name():
    print("update player name")

def check_for_player_name(name):
    print(name)

# Update Description
update_description = ttk.Label(tab_edit, text="If you are a player who would like to edit their name in the database, you can do so below.", style='TLabel')
update_description.pack(pady=(20, 0))

current_spelling_frame = ttk.Frame(tab_edit, style='TFrame')
current_spelling_frame.pack(fill='x', pady=10)
current_spelling_label = ttk.Label(current_spelling_frame, text="Current Spelling:", style='TLabel')
current_spelling_label.pack(side='left', padx=5)
current_spelling_entry = ttk.Entry(current_spelling_frame)
current_spelling_entry.pack(side='left', fill='x', expand=True, padx=5)
search_button = ttk.Button(current_spelling_frame, text="Search", command=lambda: check_for_player_name(current_spelling_entry.get()), style='TButton')
search_button.pack(side='left', padx=5)

new_spelling_frame = ttk.Frame(tab_edit, style='TFrame')
new_spelling_frame.pack(fill='x', pady=10)
new_spelling_label = ttk.Label(new_spelling_frame, text="New Spelling:", style='TLabel')
new_spelling_label.pack(side='left', padx=5)
new_spelling_entry = ttk.Entry(new_spelling_frame)
new_spelling_entry.pack(side='left', fill='x', expand=True, padx=5)
submit_button = ttk.Button(new_spelling_frame, text="Submit", command=update_player_name, style='TButton')
submit_button.pack(side='left', padx=5)

# Tab 5: Upload File
tab_upload = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_upload, text="Upload")

#Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # call function to upload file to database
        round = linparser.read_file(file_path)
        linparser.insert_data(round, db)

# Upload File Description
upload_description = ttk.Label(tab_upload, text="You can upload data for bridge tournaments using .lin files only", style='TLabel')
upload_description.pack(pady=(20, 0))

# Upload File Button
upload_button = ttk.Button(tab_upload, text="Upload File", command=upload_file, style='TButton')
upload_button.pack(pady=10)



#bridge_app = BridgeGameApp(tab_play_by_play)
root.mainloop()


