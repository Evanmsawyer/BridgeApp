SET DELIMITER $$
CREATE PROCEDURE BoardsPerTournament()
BEGIN
  SELECT TournamentName, COUNT(*) 
  FROM bridgedb.Board 
  NATURAL JOIN bridgedb.Round
  GROUP BY TournamentName;
END$$
SET DELIMITER ;
