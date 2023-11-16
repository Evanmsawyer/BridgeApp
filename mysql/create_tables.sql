
-- SQL commands to generate the bridge app database tables.

-- Creating the Team table
CREATE TABLE Team (
    Name VARCHAR(255) PRIMARY KEY
);

-- Creating the Player table
CREATE TABLE Player (
    Name VARCHAR(255) PRIMARY KEY,
    TeamName VARCHAR(255),
    FOREIGN KEY (TeamName) REFERENCES Team(Name)
);

-- Creating the Tournament table
--CREATE TABLE Tournament (
--    Name VARCHAR(255) PRIMARY KEY
--);

-- Creating the Board table
CREATE TABLE Board (
    BoardID INT PRIMARY KEY,
    RoundID INT,
    Dealer CHAR(1),
    Vulnerability VARCHAR(255)
    FOREIGN KEY (RoundID) REFERENCES Round(RoundID),
);

-- Creating the Table table
CREATE TABLE TableEntity (
    TableID VARCHAR(255) PRIMARY KEY,
    PairedTableName VARCHAR(255),
    BoardID INT,
    BidPhase TEXT,
    FirstBid VARCHAR(255),
    LastBid VARCHAR(255),
    Result VARCHAR(255),
    RawScore INT,
    FOREIGN KEY (PairedTableName) REFERENCES TableEntity(TableID),
    FOREIGN KEY (BoardID) REFERENCES Board(BoardID)
);

-- Creating the PlaysTable table
CREATE TABLE PlaysTable (
    TableName VARCHAR(255),
    Seat CHAR(1),
    PlayerName VARCHAR(255),
    FOREIGN KEY (TableName) REFERENCES TableEntity(TableID),
    FOREIGN KEY (PlayerName) REFERENCES Player(Name)
);

-- Creating the Round table
CREATE TABLE Round (
    RoundID INT PRIMARY KEY,
    TournamentName VARCHAR(255),
    TeamOneName VARCHAR(255),
    TeamTwoName VARCHAR(255),
    --Date DATE,
    FOREIGN KEY (TeamOneName) REFERENCES Team(Name),
    FOREIGN KEY (TeamTwoName) REFERENCES Team(Name),
    FOREIGN KEY (TournamentName) REFERENCES Tournament(Name)
);

-- Creating the Trick table
CREATE TABLE Trick (
    TrickNumber INT,
    TableName VARCHAR(255),
    FirstSeat CHAR(1),
    WinningSeat CHAR(1),
    Play TEXT
    FOREIGN KEY (TableName) REFERENCES TableEntity(TableID),
);

-- Creating the Hands table
CREATE TABLE Hands (
    Position TEXT,
    Spades TEXT,
    Hearts TEXT,
    Diamonds TEXT,
    Clubs TEXT,
    HighCardPoints INT,
    SuitDistribution TEXT,
    Vulnerability VARCHAR(255)
);
