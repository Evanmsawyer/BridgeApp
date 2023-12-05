SET DELIMITER $$
CREATE PROCEDURE TotalTricksByPlayer(PlayerNameInput VARCHAR(255), TeamNameInput VARCHAR(255)) 
BEGIN
    SELECT count(*)
    FROM (SELECT TableID, Seat FROM BridgeDB.PlaysTable WHERE PlayerName = PlayerNameInput AND TeamName = TeamNameInput) AS T
    NATURAL JOIN BridgeDB.Trick
    WHERE T.Seat = WinningSeat;
END$$
SET DELIMITER ;

