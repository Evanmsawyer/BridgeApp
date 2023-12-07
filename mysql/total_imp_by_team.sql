CREATE  PROCEDURE `TotalImpByTeam`()
BEGIN
	SELECT TeamName, SUM(Imp) AS TotalImp
	FROM ((
	SELECT TeamOneName AS TeamName, SUM(TeamOneImp) AS Imp
	FROM BridgeDB.Board NATURAL JOIN BridgeDB.Round
	GROUP BY TeamOneName)
	UNION (
	SELECT TeamTwoName AS TeamName, SUM(TeamTwoImp) AS Imp
	FROM BridgeDB.Board NATURAL JOIN BridgeDB.Round
	GROUP BY TeamTwoName)) AS T
	GROUP BY TeamName
	ORDER BY TotalImp DESC;
END