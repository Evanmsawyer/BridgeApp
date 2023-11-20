SET DELIMITER $$
CREATE PROCEDURE PlayerSearch(@TeamNameInput VARCHAR(255)) 
AS BEGIN
    SELECT * FROM bridgedb.Player WHERE TeamName = @TeamNameInput;
END$$
SET DELIMITER ;