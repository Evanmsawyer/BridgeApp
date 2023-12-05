SET DELIMITER $$
CREATE PROCEDURE RawScoreSearch(RawScoreInputLow INT, RawScoreInputHi INT) 
BEGIN
    SELECT * FROM BridgeDB.TableEntity WHERE RawScore BETWEEN RawScoreInputLow AND RawScoreInputHi;
END$$
SET DELIMITER ;
