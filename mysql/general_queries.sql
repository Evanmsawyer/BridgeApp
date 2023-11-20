--Search board number
SELECT * FROM Board WHERE BoardID = [INPUT];

--Dealer 
SELECT Dealer FROM Board WHERE BoardID = [INPUT];

--Seat
SELECT Seat FROM PlaysTable WHERE TableID = [INPUT];

--Vulnerability
SELECT * FROM Hands WHERE Vulnerability = [Your Vulnerability Type];

--High-Card Points 
SELECT * FROM Hands WHERE HighCardPoints >= [Your Point Threshold];

--Suit Distribution
SELECT Position, Spades, Hearts, Diamonds, Clubs FROM Hands;

--Starting bid 
SELECT FirstBid FROM TableEntity WHERE TableID = [Your Table ID];

--Ending bid
SELECT LastBid FROM TableEntity WHERE TableID = [Your Table ID];

--Board where slam was made 
SELECT Board.BoardID FROM Board JOIN TableEntity ON Board.BoardID = TableEntity.BoardID WHERE TableEntity.LastBid IN ('6', '7') AND TableEntity.Result = 'Made';

--Raw Score
SELECT RawScore FROM TableEntity WHERE TableID = [Your Table ID];

--Tournament Name
SELECT * FROM Tournament WHERE Name = [Your Tournament Name];

--Total Boards
SELECT COUNT(*) FROM Board WHERE TournamentName = [Your Tournament Name];

--Round Searches
SELECT * FROM Round WHERE TournamentName = [Your Tournament Name];

--Player Searches
SELECT * FROM Player WHERE Name = [Player Name];

--Team Name Search
SELECT * FROM Team WHERE Name = [Team Name];

--Complex Searches
--Search for all boards where slam was bid and made
SELECT TableEntity.BoardID, TableEntity.FirstBid, TableEntity.LastBid
FROM bridgedb.TableEntity
WHERE REGEXP_LIKE(TableEntity.Result, '^[6-7].[+=].*$');

--List of boards where the same contract bid in both rooms but one team made it and the other did not
SELECT t1.BoardID
FROM bridgedb.TableEntity AS t1
JOIN bridgedb.TableEntity AS t2 ON t1.PairedTableID = t2.TableID
WHERE t1.LastBid = t2.LastBid AND t1.Result <> t2.Result;

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
SELECT BoardID
FROM bridgedb.hands
WHERE Hearts = '' OR Spades = '' OR Diamonds = '' OR Clubs = '';

--List play where a game contract was bid and made >= 400 and the declarer+dummy had <= 25 HCP
SELECT BoardID
FROM bridgedb.hands
NATURAL JOIN bridgedb.TableEntity
WHERE TableEntity.RawScore >= 400 AND Player.HighCardPoints < 25;


--TOD:
--List boards with a successful sacrifice
--Number of Bids
--Slams Made in One Room but Not the Other
--IMP score search
--Total Tricks Won Career
--If they played dummy
--Starting vs. Ending Score of Segments
--Total Tournaments Won






