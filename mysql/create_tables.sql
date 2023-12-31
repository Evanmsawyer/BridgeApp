CREATE DATABASE IF NOT EXISTS BridgeDB;
DROP TABLE IF EXISTS Hands;
DROP TABLE IF EXISTS PlaysTable;
DROP TABLE IF EXISTS Trick;
DROP TABLE IF EXISTS TableEntity;
DROP TABLE IF EXISTS Board;
DROP TABLE IF EXISTS Round;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Team;

-- For position: 1 = South, 2 = West, 3 = East, 4 = North

CREATE TABLE Team (
    Name VARCHAR(255) PRIMARY KEY
);
-- Creating the Player table
CREATE TABLE Player (
    Name VARCHAR(255),
    TeamName VARCHAR(255),
    FOREIGN KEY (TeamName) REFERENCES Team(Name),
    PRIMARY KEY(Name, TeamName)
);

-- Creating the Round table
CREATE TABLE Round (
    RoundID INT PRIMARY KEY,
    TournamentName VARCHAR(255),
    TeamOneName VARCHAR(255),
    TeamTwoName VARCHAR(255),
    FOREIGN KEY (TeamOneName) REFERENCES Team(Name),
    FOREIGN KEY (TeamTwoName) REFERENCES Team(Name)
);

-- Creating the Board table
CREATE TABLE Board (
    BoardID INT PRIMARY KEY,
    RoundID INT,
    Dealer INT,
    Vulnerability CHAR(1),
    TeamOneImp INT,
    TeamTwoImp INT,
    FOREIGN KEY (RoundID) REFERENCES Round(RoundID)
);

-- Creating the Table table
CREATE TABLE TableEntity (
    TableID INT PRIMARY KEY,
    PairedTableID INT,
    BoardID INT,
    BidPhase TEXT,
    FirstBid VARCHAR(10),
    LastBid VARCHAR(10),
    Result VARCHAR(10),
    RawScore INT,
    FOREIGN KEY (PairedTableID) REFERENCES TableEntity(TableID),
    FOREIGN KEY (BoardID) REFERENCES Board(BoardID)
);

-- Creating the PlaysTable table, delay constraint checking for TableName 
CREATE TABLE PlaysTable (
    TableID INT,
    Seat INT,
    PlayerName VARCHAR(255),
    TeamName VARCHAR(255),
    FOREIGN KEY (TableID) REFERENCES TableEntity(TableID),
    FOREIGN KEY (PlayerName, TeamName) REFERENCES Player(Name, TeamName)
);

-- Creating the Trick table
CREATE TABLE Trick (
    TrickNumber INT,
    TableID INT,
    FirstSeat INT,
    WinningSeat INT,
    Play VARCHAR(8),
    FOREIGN KEY (TableID) REFERENCES TableEntity(TableID)
);

-- Creating the Hands table
CREATE TABLE Hands (
    BoardID INT,
    Position INT,
    Spades VARCHAR(13),
    Hearts VARCHAR(13),
    Diamonds VARCHAR(13),
    Clubs VARCHAR(13),
    HighCardPoints INT,
    PRIMARY KEY(Position, BoardID),
    FOREIGN KEY (BoardID) REFERENCES Board(BoardID)
);