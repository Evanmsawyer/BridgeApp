SET DELIMITER $$
CREATE PROCEDURE RawScoreSearch(@RawScoreInputLow INT, @RawScoreInputHi INT) 
AS BEGIN
    SELECT * FROM bridgedb.TableEntity WHERE RawScore BETWEEN @RawScoreInputLow AND @RawScoreInputHi;
END$$
SET DELIMITER ;