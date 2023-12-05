SET DELIMITER $$
CREATE PROCEDURE StartingBidSearch(StartingBidInput VARCHAR(10)) 
BEGIN
    SELECT * FROM BridgeDB.TableEntity WHERE SUBSTRING(FirstBid, 3, 2) = StartingBidInput;
END$$
SET DELIMITER ;
