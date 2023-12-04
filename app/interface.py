import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import pandas as pd
from PIL import Image, ImageTk
import os
import json
from dbCommunicator import DBConnector

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
global bridge_app 


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
    criteria = criteria_combobox.get()
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
            print(f"Procedure: {procedure_name}, Parameters: {parameters}")
            if procedure_name == "Tournament":
                #Test Data: 2013 USBC USA2 Final
                procedure_name = "TableInTournament"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Tricks":
                #Test Data: 
                procedure_name = "TotalTricksByPlayer"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "HCP":
                procedure_name = "HCPSearchInRange"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Last Bid":
                procedure_name = "EndingBidSearch"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Board ID":
                procedure_name = "BoardSearch"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Player":
                procedure_name = "PlayerSearch"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Dealer":
                procedure_name = "DealerSearch"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Players By Team":
                procedure_name = "PlayerSearchByTeam"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Seat":
                procedure_name = "GetSeat"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Score":
                procedure_name = "RawScoreSearch"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
                update_result_view(columns, data)
            elif procedure_name == "Slams":
                procedure_name = "SlamBidAndMade"
                columns, data = db.execute_stored_procedure(procedure_name, (parameters,))
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

criteria_options = ['Player', 'HCP', 'First Bid', 'Last Bid', 
                    'Board ID', 'Tournament', 'Tricks', 'Slams', 'Players By Team', 
                    'Seat', 'Dealer', 'Score']
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

        if 'bridge_app' in globals() and bridge_app is not None:
            del bridge_app
        bridge_app = BridgeGameApp(currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks)

result_tree.bind("<<TreeviewSelect>>", on_tree_selection)

#result_tree.heading("Column1", text="")
#result_tree.column("Column1", width=120)


# Tab 2: Play-by-Play Details
tab_play_by_play = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_play_by_play, text="Play-by-Play")

script_dir = os.path.dirname(os.path.abspath(__file__))
cards_folder = 'assets/cards'
cards_path = os.path.join(script_dir, cards_folder)

class BridgeGameApp:
    def __init__(self, currentTable, currentNHand, currentSHand, currentEHand, currentWHand, currentTricks):
        self.currentTricks = currentTricks
        # Initialize game state
        self.current_play = 0
        # Define the font to use for card display
        self.card_font = tk.font.Font(family='Helvetica', size=12, weight='bold')

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

        self.player_frames = {
            1: self.north_frame,
            2: self.east_frame,
            3: self.south_frame,
            4: self.west_frame
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

        # Sample data
        self.hands = {
            0: currentNHand[0],
            1: currentEHand[0],
            2: currentSHand[0],
            3: currentWHand[0],
        }

        # Display initial hands
        self.display_hand(self.north_frame, self.hands[0], horizontal=True)
        self.display_hand(self.east_frame, self.hands[1], horizontal=False)
        self.display_hand(self.south_frame, self.hands[2], horizontal=True)
        self.display_hand(self.west_frame, self.hands[3], horizontal=False)

        # Placeholder for card labels (to display card images)
        self.center_cards = []

        # Initialize or load a game state here
        self.center_label = tk.Label(self.center_frame, text='', font=self.card_font, bg='white')
        self.center_label.pack(expand=True)

         # Add navigation buttons
        self.back_button = tk.Button(self.container_frame, text="Back", command=self.move_back)
        self.back_button.grid(row=3, column=0, sticky='ew')

        self.next_button = tk.Button(self.container_frame, text="Next", command=self.move_next)
        self.next_button.grid(row=3, column=2, sticky='ew')

        # Initialize the current play index
        self.current_play_index = 0

    def update_center(self, cards_played, remove=False):
        # Add or remove cards from the center display based on the direction of the move
        if remove:
            # If moving backward, remove the last played cards from the display
            self.center_cards = self.center_cards[:-len(cards_played)]
        else:
            # If moving forward, add the new cards to the display
            self.center_cards.extend(list(cards_played))

        # Update the center label with the current cards
        center_text = ''.join(self.center_cards) + ' '
        self.center_label.config(text=center_text)

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

    def update_hand(self, player, cards_played, remove=False):
        player = int(player-1)
        hand_tuple = self.hands.get(player)
        if hand_tuple is None:
            # Handle error: no hand found for this player number
            print(f"No hand found for player {player}")
            return
        
        hand_list = list(hand_tuple)

        for card in cards_played:
            suit_index = 'SHDC'.index(card[0])  
            suit_hand = hand_list[suit_index]
            if remove:
                hand_list[suit_index] = suit_hand + card[1:]
            else:
                hand_list[suit_index] = suit_hand.replace(card[1:], '')
        self.hands[player] = tuple(hand_list)
        print(self.player_frames)
        print(player)
        self.display_hand(self.player_frames[player], self.hands[player], horizontal=player in [1, 3])

    """
    def play_game(self, plays):
        # Loop through the plays and update hands accordingly
        for play in plays.values():
            player, cards_played = play[2], play[4]
            self.update_hand(player, [cards_played[i:i+2] for i in range(0, len(cards_played), 2)])"""

    def move_next(self):
        if self.current_play_index < len(self.currentTricks) - 1:
            self.current_play_index += 1
            self.play_current()

    def move_back(self):
        if self.current_play_index > 0:
            self.current_play_index -= 1
            self.play_current(backward=True)

    def find_player_with_card(self, card):
        suit_order = {'S': 0, 'H': 1, 'D': 2, 'C': 3}
        for player, hand_tuple in self.hands.items():
            suit = card[0]  # The suit of the card ('S', 'H', 'D', 'C')
            value = card[1:]  # The value of the card ('6', 'A', 'Q', etc.)

            suit_index = suit_order.get(suit)  # Get the index of the suit in the tuple
            if suit_index is not None and value in hand_tuple[suit_index]:
                return player
        return None  # Return None if the card is not found in any hand

    def play_current(self, backward=False):
        # Retrieve the current play
        current_play = self.currentTricks[self.current_play_index]

        # Determine the player and the cards played
        player, cards_played = current_play[2], current_play[4]

        # If we are moving backward, remove the cards from the center and add them back to the player's hand
        # If we are moving forward, remove the cards from the player's hand and add them to the center
        if backward:
            self.update_center(cards_played, remove=True)
            for card in cards_played:
                print(card)
                playerscard = self.find_player_with_card(card)
                print(playerscard)
                self.update_hand(player, playerscard, remove=True)
        else:
            self.update_center(cards_played, remove=False)
            for card in cards_played:
                print(card)
                playerscard = self.find_player_with_card(card)
                self.update_hand(player, playerscard, remove=False)



# Tab 3: Statistics Details
tab_statistics = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_statistics, text="Statistics")

# Tab 4: Upload File
tab_upload = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_upload, text="Upload")

# Tab 5: Edit
tab_edit = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_edit, text="Edit")


def fetch_statistics():
    total_tricks = db.execute_query("SELECT COUNT(*) FROM Tricks")
    return {
        #"North Player Total Tricks": total_tricks,
    }

# Function to update statistics view
def update_statistics_view():
    stats = fetch_statistics()

    for i, (stat_name, stat_value) in enumerate(stats.items()):
        ttk.Label(tab_statistics, text=f"{stat_name}:", style='TLabel').grid(row=i, column=0, sticky='W', padx=5, pady=5)
        ttk.Label(tab_statistics, text=str(stat_value), style='TLabel').grid(row=i, column=1, sticky='W', padx=5, pady=5)


#bridge_app = BridgeGameApp(tab_play_by_play)
root.mainloop()


