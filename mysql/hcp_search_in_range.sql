SET DELIMITER $$
CREATE PROCEDURE HCPSearchInRange(Upper INT, Lower INT) 
BEGIN
    SELECT * FROM bridgedb.Hands WHERE HighCardPoints >= Upper AND HighCardPoints <= Lower;
END$$
SET DELIMITER ;
