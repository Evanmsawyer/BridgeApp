DELIMITER $$
CREATE  PROCEDURE UpdateName(OldPlayer VARCHAR(255), NewPlayer VARCHAR(255), TeamNameIn VARCHAR(255))
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		SET FOREIGN_KEY_CHECKS = 1;
		ROLLBACK;
        RESIGNAL;
	END;
    START TRANSACTION;
	SET FOREIGN_KEY_CHECKS = 0;
    IF EXISTS (SELECT * FROM Player WHERE Name = NewPlayer AND TeamName = TeamNameIn) THEN
		DELETE FROM Player
        WHERE Name = OldPlayer AND TeamName = TeamNameIn;
	ELSE
		UPDATE Player
		SET Name = NewPlayer
		WHERE Name = OldPlayer AND TeamName = TeamNameIn;
	END IF;
    UPDATE PlaysTable
    SET PlayerName = NewPlayer
    WHERE PlayerName = OldPlayer AND TeamName = TeamNameIn;
    SET FOREIGN_KEY_CHECKS = 1;
    IF EXISTS (SELECT * 
				FROM PlaysTable AS t1 JOIN PlaysTable AS t2
				ON t1.TableID = t2.TableID AND t1.PlayerName = t2.PlayerName AND t1.TeamName = t2.TeamName
                WHERE t1.Seat != t2.Seat AND t1.PlayerName = NewPlayer AND t1.TeamName = TeamNameIn) THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Repeat player at table';
	ELSEIF NewPlayer = '' THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Blank NewPlayer string';
	ELSE
		COMMIT;
	END IF;
END$$
DELIMITER ;
