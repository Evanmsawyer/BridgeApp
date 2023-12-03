SET DELIMITER $$
CREATE PROCEDURE PlayerSearchByTeam(TeamNameInput VARCHAR(255)) 
BEGIN
    SELECT * FROM BridgeDB.Player WHERE TeamName = TeamNameInput;
END$$
SET DELIMITER ;

