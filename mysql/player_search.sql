SET DELIMITER $$
CREATE PROCEDURE PlayerSearch(@PlayerNameInput VARCHAR(255)) 
AS BEGIN
    SELECT * FROM bridgedb.Player WHERE Name = @PlayerNameInput;
END$$
SET DELIMITER ;