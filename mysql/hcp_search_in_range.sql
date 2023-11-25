SET DELIMITER $$
CREATE PROCEDURE HCPSearchInRange(@Upper INT, @Lower INT) 
AS BEGIN
    SELECT * FROM bridgedb.Hands WHERE HighCardPoints >= @Upper AND HighCardPoints <= @Lower;
END$$
SET DELIMITER ;