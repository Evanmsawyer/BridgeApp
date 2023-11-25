SET DELIMITER $$
CREATE PROCEDURE TableInTournament(@TournamentName VARCHAR(255)) 
AS BEGIN
    SELECT TableID 
    FROM bridgedb.Round 
    NATURAL JOIN bridgedb.Board 
    NATURAL JOIN bridgedb.TableEntity 
    WHERE TournamentName = @TournamentName;
END$$
SET DELIMITER ;