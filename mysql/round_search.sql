SET DELIMITER $$
CREATE PROCEDURE RoundSearch(@TournamentName VARCHAR(255)) 
AS BEGIN
    SELECT * FROM bridgedb.Round WHERE TournamentName = @TournamentName;
END$$
SET DELIMITER ;