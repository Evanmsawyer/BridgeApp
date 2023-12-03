SET DELIMITER $$
CREATE PROCEDURE DealerSearch(DealerInput INT) 
AS BEGIN
    SELECT * FROM bridgedb.Board WHERE Dealer = DealerInput;
END$$
SET DELIMITER ;
