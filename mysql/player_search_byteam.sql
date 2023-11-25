SET DELIMITER $$
CREATE PROCEDURE PlayerSearchByTeam(@TeamNameInput VARCHAR(255)) 
AS BEGIN
    SELECT * FROM bridgedb.Player WHERE TeamName = @TeamNameInput;
END$$
SET DELIMITER ;

