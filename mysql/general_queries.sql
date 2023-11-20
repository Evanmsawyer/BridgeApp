--Search board number
SELECT * FROM bridgedb.Board WHERE BoardID = [INPUT];

--Get boards with the given dealer
 SELECT * FROM bridgedb.Board WHERE Dealer = [INPUT];

--Get seat for a specific player on a specific team at a specific table
SELECT Seat FROM bridgedb.PlaysTable WHERE TableID = [INPUT] AND PlayerName = [INPUT] AND TeamName = [INPUT];

--Get boards where the given team is vulnerable (score bonus if they win, score penalty if they lose)
SELECT * FROM bridgedb.Board WHERE Vulnerability IN ([INPUT], 'B');

--Get hands where the high card points are in a given range
SELECT * FROM bridgedb.Hands WHERE HighCardPoints >= [lower] AND HighCardPoints <= [upper];

--Get hands with a given suit distribution
SELECT * 
FROM bridgedb.Hands 
WHERE LENGTH(Spades) = [INPUT] AND LENGTH(Hearts) = [INPUT] AND LENGTH(Diamonds) = [INPUT] AND LENGTH(Clubs) = [INPUT];

--Get tables with a given starting bid
SELECT * FROM bridgedb.TableEntity WHERE SUBSTRING(FirstBid, 3, 2) = [INPUT];

--Get tables with a given ending bid
SELECT LastBid FROM bridgedb.TableEntity WHERE SUBSTRING(LastBid, 3, 2) = [INPUT];

--Get tables with a raw score within the given range
SELECT * FROM bridgedb.TableEntity WHERE RawScore BETWEEN [low] AND [hi];

--Get tables in a specific tournament
SELECT TableID 
FROM bridgedb.Round 
NATURAL JOIN bridgedb.Board 
NATURAL JOIN bridgedb.TableEntity 
WHERE TournamentName = [INPUT];

--Total boards for each tournament
SELECT TournamentName, COUNT(*) 
FROM bridgedb.Board 
NATURAL JOIN bridgedb.Round
GROUP BY TournamentName

--Get all players with a given name
SELECT * FROM bridgedb.Player WHERE Name = [INPUT];

--Get all players on a given team
SELECT * FROM bridgedb.Player WHERE TeamName = [INPUT];

--Total tricks won for each player
SELECT count(*)
FROM (SELECT TableID FROM bridgedb.PlaysTable WHERE PlayerName = [INPUT] AND TeamName = [INPUT])
NATURAL JOIN bridgedb.Trick
WHERE Seat = WinningSeat

--Complex Searches
--Search for all boards where slam was bid and made
SELECT TableEntity.BoardID, TableEntity.FirstBid, TableEntity.LastBid
FROM bridgedb.TableEntity
WHERE REGEXP_LIKE(TableEntity.Result, '^[6-7].[+=].*$');

--List of boards where the same contract bid in both rooms but one team made it and the other did not
SELECT DISTINCT t1.BoardID
FROM bridgedb.TableEntity AS t1
JOIN bridgedb.TableEntity AS t2 ON t1.PairedTableID = t2.TableID
WHERE SUBSTRING(t1.LastBid, 3, 2) = SUBSTRING(t2.LastBid, 3, 2) AND SUBSTRING(t1.Result, 3, 1) <> SUBSTRING(t2.Result, 3, 1);

--List of boards where the same contract bid in both rooms with different results and different opening lead
--Probably don't do this one - a less strict version of this search returned no results
    --SELECT b1.BoardID
    --FROM TableEntity AS t1
    --JOIN TableEntity AS t2 ON t1.PairedTableID = t2.TableID
    --JOIN Board b1 ON t1.BoardID = b1.BoardID
    --JOIN Board b2 ON t2.BoardID = b2.BoardID
    --JOIN Trick tr1 ON t1.TableID = tr1.TableID
    --JOIN Trick tr2 ON t2.TableID = tr2.TableID
    --WHERE t1.LastBid = t2.LastBid AND t1.Result != t2.Result AND tr1.FirstSeat != tr2.FirstSeat;

--List boards where any hand had no cards of a given suit
SELECT DISTINCT BoardID
FROM bridgedb.hands
WHERE Hearts = '' OR Spades = '' OR Diamonds = '' OR Clubs = '';

--List play where a game contract was bid and made >= 400 and the declarer+dummy had <= 25 HCP
WITH Team_HCP(BoardID, Value, Position) AS
   (SELECT h1.BoardID, h1.HighCardPoints + h2.HighCardPoints, h1.Position
    FROM bridgedb.hands AS h1, bridgedb.hands AS h2
    WHERE h1.BoardID = h2.BoardID AND ((h1.Position = 'N' AND h2.Position = 'S')
      OR (h1.Position = 'E' AND h2.Position = 'W')) 
      AND h1.HighCardPoints + h2.HighCardPoints <= 25)
SELECT TableID
FROM Team_HCP
NATURAL JOIN (SELECT * FROM bridgedb.TableEntity WHERE TableEntity.RawScore >= 400) AS t1
WHERE ((Team_HCP.Position = 'N' AND SUBSTRING(t1.LastBid, 1, 1) IN ('S', 'N'))
    OR (Team_HCP.Position = 'E' AND SUBSTRING(t1.LastBid, 1, 1) IN ('E', 'W')));

--List all tricks in order for a specific table
SELECT *
FROM bridgedb.trick
WHERE trick.TableID = [INPUT]
ORDER BY trick.TrickNumber ASC

--List all tables where a trump card was played in each trick
--Incomplete, probably don't submit this
WITH trump(TableID, suit) AS
    (SELECT TableID, SUBSTRING(t1.LastBid, 4, 1)
    FROM bridgedb.tableentity AS t1)
SELECT TableID
FROM bridgedb.trick NATURAL JOIN trump
WHERE LOCATE(trick.play, trump.suit) <> 0
--TOD:
--List boards with a successful sacrifice
--Number of Bids
--Slams Made in One Room but Not the Other
--IMP score search
--Total Tricks Won Career
--If they played dummy
--Starting vs. Ending Score of Segments
--Total Tournaments Won