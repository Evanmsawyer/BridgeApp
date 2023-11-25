SET DELIMITER $$
CREATE PROCEDURE GetSeat(@TableIDInput INT, @PlayerNameInput varchar(255), @TeamNameInput varchar(255))
AS BEGIN
    SELECT Seat FROM bridgedb.PlaysTable WHERE TableID = @TableIDInput AND PlayerName = @PlayerNameInput AND TeamName = @TeamNameInput;
END$$
SET DELIMITER ;