import csv
import mysql.connector
import json

#set CSV file path
table_path = "./CSVs/table.csv"
#connect to database
with open("connector_config.json", "r") as f:
    config = json.load(f)
connection_config = config["mysql"]
data_base = mysql.connector.connect(**connection_config)
#prepare a cursor object
cursor_object = data_base.cursor()
#get data from database
query = """
SELECT TableID
FROM bridgedb.tableentity
"""
cursor_object.execute(query)
db_results = cursor_object.fetchall()
#convert results from tuples to integers
db_results = [int(x[0]) for x in db_results]
print("calculating diff")
diff = [x for x in range(197344) if x not in db_results]
print("done")
with open("diff.txt", mode="w", encoding="UTF-8") as f:
    for x in diff:
        print(x, file=f)
