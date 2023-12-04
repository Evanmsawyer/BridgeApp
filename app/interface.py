import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk
import os
import json
from dbCommunicator import DBConnector
import enum

db = DBConnector()
result_tree = None
root = None
tab_search = None
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
        print(currentTable)
        currentNHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (3, table_id))
        print(currentNHand)
        currentSHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (1, table_id))
        print(currentSHand)
        currentEHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (4, table_id))
        print(currentEHand)
        currentWHand = db.execute_query("SELECT Spades, Hearts, Diamonds, Clubs, HighCardPoints from Hands natural join TableEntity where Position = %s and TableID = %s"% (2, table_id))
        print(currentWHand)
        currentTricks = db.execute_query("SELECT * FROM Trick WHERE Trick.TableID = %s ORDER BY Trick.TrickNumber ASC"% (table_id,))
        print(currentTricks)

        del bridge_app
        bridge_app = BridgeGameApp(tab_play_by_play)

result_tree.bind("<<TreeviewSelect>>", on_tree_selection)

#result_tree.heading("Column1", text="")
#result_tree.column("Column1", width=120)


# Tab 2: Play-by-Play Details
tab_play_by_play = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_play_by_play, text="Play-by-Play")

class BridgeGameApp:
    def __init__(self, frame):
        # Load card images
        self.card_images = self.load_card_images()

        # Initialize game state
        self.current_play = 0

        # Create buttons
        self.back_button = tk.Button(root, text="Back", command=self.move_back)
        self.back_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(root, text="Next", command=self.move_next)
        self.next_button.pack(side=tk.RIGHT)

        # Create a frame to display cards
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Placeholder for card labels (to display card images)
        self.card_labels = []

        # Initialize or load a game state here
        self.game_state = [...]

    def load_card_images(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cards_folder = 'assets/cards'
        cards_path = os.path.join(script_dir, cards_folder)
        card_images = {}
        #Heart is 2, Diamonad is 4, Spade is 5, Club is 7
        for suit in ['S', 'D', 'C', 'H']:
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                card_name = suit + value
                image_path = os.path.join(cards_path, card_name + '.png')
                image = Image.open(image_path)
                card_images[card_name] = ImageTk.PhotoImage(image)
        return card_images

    def display_cards(self):
        # Clear existing cards
        for label in self.card_labels:
            label.destroy()

        # Display cards for the current play
        cards = self.game_state[self.current_play]
        self.card_labels = []
        for card in cards:
            label = tk.Label(self.card_frame, image=self.card_images[card])
            label.pack(side=tk.LEFT)
            self.card_labels.append(label)

    def move_next(self):
        if self.current_play < len(self.game_state) - 1:
            self.current_play += 1
            self.display_cards()

    def move_back(self):
        if self.current_play > 0:
            self.current_play -= 1
            self.display_cards()


# Tab 3: Statistics Details
tab_statistics = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_statistics, text="Statistics")

# Tab 4: Upload File
tab_upload = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_upload, text="Upload")

#Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # call function to upload file to database
        print("insert the data")

# Upload File Description
upload_description = ttk.Label(tab_upload, text="You can upload data for bridge tournaments using .lin files only", style='TLabel')
upload_description.pack(pady=(20, 0))

# Upload File Button
upload_button = ttk.Button(tab_upload, text="Upload File", command=upload_file, style='TButton')
upload_button.pack(pady=10)

# Tab 5: Edit
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


bridge_app = BridgeGameApp(tab_play_by_play)
root.mainloop()





