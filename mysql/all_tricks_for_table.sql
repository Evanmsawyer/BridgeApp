SET DELIMITER $$
CREATE PROCEDURE TricksForTable(TableIdInput INT) 
BEGIN
    SELECT *
    FROM bridgedb.trick
    WHERE trick.TableID = TableIdInput
    ORDER BY trick.TrickNumber ASC;
END$$
SET DELIMITER ;
