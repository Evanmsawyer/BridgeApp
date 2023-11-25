SET DELIMITER $$
CREATE PROCEDURE EndingBidSearch(@EndingBidInut VARCHAR(10)) 
AS BEGIN
    SELECT * FROM bridgedb.TableEntity WHERE SUBSTRING(LastBid, 3, 2) = @EndingBidInut;
END$$
SET DELIMITER ;