--List play where a game contract was bid and made >= 400 and the declarer+dummy had <= 25 HCP
SET DELIMITER $$
CREATE PROCEDURE UnderDogSearch() 
BEGIN
  WITH Team_HCP(BoardID, Value, Position) AS
    (SELECT h1.BoardID, h1.HighCardPoints + h2.HighCardPoints, h1.Position
      FROM bridgedb.hands AS h1, bridgedb.hands AS h2
      WHERE h1.BoardID = h2.BoardID AND ((h1.Position = 'N' AND h2.Position = 'S')
        OR (h1.Position = 'E' AND h2.Position = 'W')) 
        AND h1.HighCardPoints + h2.HighCardPoints <= 25)
  SELECT TableID
  FROM Team_HCP
  NATURAL JOIN (SELECT * FROM bridgedb.TableEntity WHERE TableEntity.RawScore >= 400) AS t1
  WHERE ((Team_HCP.Position = 'N' AND SUBSTRING(t1.LastBid, 1, 1) IN ('S', 'N'))
      OR (Team_HCP.Position = 'E' AND SUBSTRING(t1.LastBid, 1, 1) IN ('E', 'W')));
END$$
SET DELIMITER ;