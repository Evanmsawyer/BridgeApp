import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk
import os
import json
from dbCommunicator import DBConnector

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

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # You can add your logic here to handle the file
        print(f"File selected: {file_path}")

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

#Upload button in the top right corner
upload_button = ttk.Button(main_frame, text="Upload File", command=upload_file, style='TButton')
upload_button.pack(side='right', padx=5, pady=5)

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

criteria_options = ['Player', 'HCP', 'First Bid', 'Last Bid', 'Board ID', 'Tournament', 'Tricks', 'Slams', 'Players By Team']
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

        print(columns)
        
        # Assuming 'TableID' is one of the columns, and we know its index
        # Replace 'table_id_index' with the actual index of 'TableID' column
        if columns and columns.index('TableID'):
            table_id_index = columns.index('TableID')
            table_id = row_data[table_id_index]
            print(f"Selected TableID: {table_id}")  # Or perform other actions with the TableID

        currentTable = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
        print(currentTable)
        currentNHand = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
        print(currentNHand)
        currentSHand = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
        print(currentSHand)
        currentEHand = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
        print(currentEHand)
        currentWHand = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
        print(currentWHand)
        currentTricks = db.execute_query("SELECT * FROM TableEntity WHERE TableID = %s"% (table_id,))
        print(currentTricks)

result_tree.bind("<<TreeviewSelect>>", on_tree_selection)

#result_tree.heading("Column1", text="")
#result_tree.column("Column1", width=120)


# Tab 2: Play-by-Play Details
tab_play_by_play = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_play_by_play, text="Play-by-Play")

class BridgeGameApp:
    def __init__(self, root, gamedata):
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
        self.card_frame = tk.Frame(root)
        self.card_frame.pack()

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
        for suit in ['2', '4', '5', '7']:
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                if value != 'J' and  value != 'K' and value != 'Q':
                    card_name = value + '.' + suit
                else:
                    card_name = value + suit
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


app = BridgeGameApp(tab_play_by_play, "")
root.mainloop()





