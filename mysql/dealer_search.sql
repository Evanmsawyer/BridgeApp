SET DELIMITER $$
CREATE PROCEDURE DealerSearch(@DealerInput char(1)) 
AS BEGIN
    SELECT * FROM bridgedb.Board WHERE Dealer = @DealerInput;
END$$
SET DELIMITER ;