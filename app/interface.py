import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import json

# Load database configuration from a JSON file
def load_db_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

db_config = load_db_config('db_config.json')

# Function to create a database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# Function to build and execute a dynamic query based on selected checkboxes
def dynamic_search():
    conditions = []
    parameters = []

    # Or we can call the sql files and store the tables for joining.
    if cb_board_id_var.get():
        board_id = entry_board_id.get()
        conditions.append("Board.BoardID = %s")
        parameters.append(board_id)

    if cb_player_name_var.get():
        player_name = entry_player_name.get()
        conditions.append("Player.Name = %s")
        parameters.append(player_name)

    if cb_first_bid_var.get():
        first_bid = entry_first_bid.get()
        conditions.append("TableEntity.FirstBid = %s")
        parameters.append(first_bid)

    if cb_last_bid_var.get():
        last_bid = entry_last_bid.get()
        conditions.append("TableEntity.LastBid = %s")
        parameters.append(last_bid)

    if cb_high_card_points_var.get():
        hcp = entry_high_card_points.get()
        conditions.append("Hands.HighCardPoints >= %s")
        parameters.append(hcp)

    if cb_suit_distribution_var.get():
        suit_dist = entry_suit_distribution.get()
        conditions.append("Hands.SuitDistribution = %s")
        parameters.append(suit_dist)

    # Building the base of the query
    base_query = """
    SELECT DISTINCT Board.BoardID, Player.Name, TableEntity.FirstBid, TableEntity.LastBid, Hands.HighCardPoints
    FROM Board
    LEFT JOIN TableEntity ON Board.BoardID = TableEntity.BoardID
    LEFT JOIN PlaysTable ON TableEntity.TableID = PlaysTable.TableName
    LEFT JOIN Player ON PlaysTable.PlayerName = Player.Name
    LEFT JOIN Hands ON Player.Name = Hands.Position
    """

    # Add WHERE clause if there are conditions
    if conditions:
        query = base_query + " WHERE " + " AND ".join(conditions)
    else:
        query = base_query

    result = run_query(query, parameters)
    update_result_view(result)


# Database query function
def run_query(query, parameters=()):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        connection.commit()
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()
        connection.close()
    return result

# Function to update the result view
def update_result_view(data):
    result_tree.delete(*result_tree.get_children())
    for row in data:
        result_tree.insert('', 'end', values=row)

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
search_input_frame.pack(fill='x', expand=False, pady=10)

# Dropdown menu for criteria
criteria_label = ttk.Label(search_input_frame, text="Select Criteria:", font=custom_font, style='TLabel')
criteria_label.pack(side='left', padx=5, pady=5)

criteria_options = ['Player', 'HCP', 'First Bid', 'Last Bid', 'Board ID']
criteria_combobox = ttk.Combobox(search_input_frame, values=criteria_options, state='readonly', font=custom_font)
criteria_combobox.pack(side='left', padx=5, pady=5)

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
result_tree = ttk.Treeview(columns=("Column1", "Column2", "Column3", "Column4"), show="headings")
result_tree.pack(fill='both', padx="10", pady="10", expand=True)

# Tab 2: Play-by-Play Details
tab_play_by_play = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_play_by_play, text="Play-by-Play")

# Tab 3: Statistics Details
tab_statistics = ttk.Frame(notebook, style='TFrame')
notebook.add(tab_statistics, text="Statistics")

root.mainloop()

# Result view setup...

# Play-by-Play Tab Content...
# Here you can add widgets and functionality to display play-by-play details

root.mainloop()


