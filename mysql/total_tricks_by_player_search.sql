SET DELIMITER $$
CREATE PROCEDURE TotalTricksByPlayer(@PlayerNameInput VARCHAR(255), @TeamNameInput VARCHAR(255)) 
AS BEGIN
    SELECT count(*)
    FROM (SELECT TableID, Seat FROM bridgedb.PlaysTable WHERE PlayerName = @PlayerNameInput AND TeamName = @TeamNameInput) AS T
    NATURAL JOIN bridgedb.Trick
    WHERE T.Seat = WinningSeat;
END$$
SET DELIMITER ;

