SET DELIMITER $$
CREATE PROCEDURE TotalTricksByPlayer(@PlayerNameInput VARCHAR(255), @TeamNameInput VARCHAR(255)) 
AS BEGIN
    SELECT count(*)
    FROM (SELECT TableID FROM bridgedb.PlaysTable WHERE PlayerName = @PlayerNameInput AND TeamName = TeamNameInput)
    NATURAL JOIN bridgedb.Trick
    WHERE Seat = WinningSeat
END$$
SET DELIMITER ;