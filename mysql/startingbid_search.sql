SET DELIMITER $$
CREATE PROCEDURE StartingBidSearch(@StartingBidInput VARCHAR(10)) 
AS BEGIN
    SELECT * FROM bridgedb.TableEntity WHERE SUBSTRING(FirstBid, 3, 2) = @StartingBidInput;
END$$
SET DELIMITER ;