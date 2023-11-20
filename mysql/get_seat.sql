SET DELIMITER $$
CREATE PROCEDURE GetSeat(@TableIDInput INT, @PlayerNameInput varchar(255), @TeamNameInput varchar(255))
AS BEGIN
    SELECT Seat FROM bridgedb.PlaysTable WHERE TableID = [INPUT] AND PlayerName = [INPUT] AND TeamName = [INPUT];
END$$
SET DELIMITER ;