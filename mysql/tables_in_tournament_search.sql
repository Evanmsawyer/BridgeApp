SET DELIMITER $$
CREATE PROCEDURE TableInTournament(InputName VARCHAR(255)) 
BEGIN
    SELECT TableID, PairedTableID, BoardID, BidPhase, FirstBid, LastBid, Result, RawScore
    FROM BridgeDB.Round 
    NATURAL JOIN BridgeDB.Board 
    NATURAL JOIN BridgeDB.TableEntity 
    WHERE TournamentName = InputName;
END$$
SET DELIMITER ;
