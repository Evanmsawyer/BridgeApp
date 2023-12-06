--List of boards where the same contract bid in both rooms but one team made it and the other did not
SET DELIMITER $$
CREATE PROCEDURE TwoBidsOneMade() 
BEGIN
    SELECT DISTINCT *
    FROM BridgeDB.TableEntity AS t1
    JOIN BridgeDB.TableEntity AS t2 ON t1.PairedTableID = t2.TableID
    WHERE SUBSTRING(t1.LastBid, 3, 2) = SUBSTRING(t2.LastBid, 3, 2) AND SUBSTRING(t1.Result, 3, 1) <> SUBSTRING(t2.Result, 3, 1);
END$$
SET DELIMITER ;