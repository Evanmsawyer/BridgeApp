--Total boards for each tournament
SELECT TournamentName, COUNT(*) 
FROM bridgedb.Board 
NATURAL JOIN bridgedb.Round
GROUP BY TournamentName