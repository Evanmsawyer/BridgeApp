SET DELIMITER $$
CREATE PROCEDURE DealerSearch(DealerInput INT) 
BEGIN
    SELECT * FROM bridgedb.Board WHERE Dealer = DealerInput;
END$$
SET DELIMITER ;
