SET DELIMITER $$
CREATE PROCEDURE BoardsInTournament(@TournamentName VARCHAR(255)) 
AS BEGIN
    SELECT *
    FROM bridgedb.Board 
    NATURAL JOIN bridgedb.Round
    WHERE TournamentName = @TournamentName;
END$$
SET DELIMITER ;