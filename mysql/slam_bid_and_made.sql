--Search for all boards where slam was bid and made
SELECT TableEntity.BoardID, TableEntity.FirstBid, TableEntity.LastBid
FROM bridgedb.TableEntity
WHERE REGEXP_LIKE(TableEntity.Result, '^[6-7].[+=].*$');