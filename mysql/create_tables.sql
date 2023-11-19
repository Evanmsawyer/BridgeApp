
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
    Vulnerability CHAR(1),
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

-- Creating the PlaysTable table
CREATE TABLE PlaysTable (
    TableName INT,
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
    TableID INT,
    FirstSeat CHAR(1),
    WinningSeat CHAR(1),
    Play CHAR(8),
    FOREIGN KEY (TableID) REFERENCES TableEntity(TableID)
);

-- Creating the Hands table
CREATE TABLE Hands (
    BoardID INT,
    Position CHAR(1),
    Spades VARCHAR(13),
    Hearts VARCHAR(13),
    Diamonds VARCHAR(13),
    Clubs VARCHAR(13),
    HighCardPoints INT,
    SuitDistribution CHAR(4),
    FOREIGN KEY (BoardID) REFERENCES Baord(BoardID)
);
