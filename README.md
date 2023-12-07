# BridgeApp

## By Evan Sawyer, Corey Reinholdtsen, and Alex Carney. 

## Requirements

### Python

Python is required to run the frontend application, as well as the scripts for data acquisition and conversion.
You can download Python [here](https://www.python.org/downloads/). After installing Python, make sure that the 
following libraries are installed. Command line arguments for installation are listed for each requirement.
- MySQL Connector for Python: `pip install mysql-connector-python`
- pandas: `pip install pandas`
- requests: `pip install requests`
- BeautifulSoup: `pip install beautifulsoup4`

### MySQL

The backend database for the application is run on MySQL. Installing MySQL Workbench is recommended as well.
The rest of this guide will assume you are using MySQL 8.0 Community Server or later, and MySQL Workbench 8.0 CE. 
You can download MySQL [here](https://dev.mysql.com/downloads/) by selecting "MySQL Community Server", and you can
download MySQL Workbench at the same link by selecting "MySQL Workbench".

## Installation

### Setting up the database

If you are connecting to an instance of the database that is already set up, you can skip to "Connecting the frontend". Otherwise, there are two ways to create the database:
creating the schema and inserting the data manually, or creating the schema and inserting the pre-acquired data via the same .sql file.

#### Inserting Data Automatically

To insert data from the provided sql dump, open the database using MySQL Workbench, then open a new query tab and select "SchemaAndDataDump.sql" from this repository's mysql directory.

#### Inserting Data Manually

To insert data manually, first create the schema by executing "SchemaOnlyDump.sql" from this repository's mysql directory, following the instructions from "Inserting Data Automatically".
After creating the schema, consult the README in the data directory for details on the data insertion process.

### Connecting the frontend

