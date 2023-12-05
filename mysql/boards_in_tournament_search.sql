SET DELIMITER $$
CREATE PROCEDURE BoardsInTournament(InputName VARCHAR(255)) 
BEGIN
    SELECT *
    FROM bridgedb.Board
    NATURAL JOIN bridgedb.Round
    WHERE TournamentName = InputName;
END$$
SET DELIMITER ;
