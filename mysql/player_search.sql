SET DELIMITER $$
CREATE PROCEDURE PlayerSearch(PlayerNameInput VARCHAR(255)) 
BEGIN
    SELECT * FROM BridgeDB.Player WHERE Name = PlayerNameInput;
END$$
SET DELIMITER ;
