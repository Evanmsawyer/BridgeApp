SET DELIMITER $$
CREATE PROCEDURE EndingBidSearch(EndingBidInput VARCHAR(10)) 
BEGIN
    SELECT * FROM bridgedb.TableEntity WHERE SUBSTRING(LastBid, 3, 2) = EndingBidInput;
END$$
SET DELIMITER ;
