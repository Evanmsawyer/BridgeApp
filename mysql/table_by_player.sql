SET DELIMITER $$
CREATE PROCEDURE table_by_player(PlayerIn VARCHAR(255), TeamIn VARCHAR(255))
BEGIN
    SELECT TableID, PairedTableID, BoardID, BidPhase, FirstBid, LastBid, Result, RawScore
    FROM BridgeDB.PlaysTable
    NATURAL JOIN BridgeDB.TableEntity
    WHERE PlayerName = PlayerIn AND TeamName = TeamIn;
END$$
SET DELIMITER ;