--List of boards where the same contract bid in both rooms but one team made it and the other did not
SELECT DISTINCT t1.BoardID
FROM bridgedb.TableEntity AS t1
JOIN bridgedb.TableEntity AS t2 ON t1.PairedTableID = t2.TableID
WHERE SUBSTRING(t1.LastBid, 3, 2) = SUBSTRING(t2.LastBid, 3, 2) AND SUBSTRING(t1.Result, 3, 1) <> SUBSTRING(t2.Result, 3, 1);