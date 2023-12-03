SET DELIMITER $$
CREATE PROCEDURE TricksForTable(TableIdInput INT) 
BEGIN
    SELECT *
    FROM BridgeDB.Trick
    WHERE Trick.TableID = TableIdInput
    ORDER BY Trick.TrickNumber ASC;
END$$
SET DELIMITER ;
