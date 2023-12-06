SET DELIMITER $$
CREATE PROCEDURE UpdateName(OldPlayer VARCHAR(255), NewPlayer VARCHAR(255), TeamNameIn VARCHAR(255))
BEGIN
	SET FOREIGN_KEY_CHECKS = 0;
	UPDATE Player
    SET PlayerName = NewPlayer
    WHERE PlayerName = OldPlayer AND TeamName = TeamNameIn;
    UPDATE PlaysTable
    SET PlayerName = NewPlayer
    WHERE PlayerName = OldPlayer AND TeamName = TeamNameIn;
    IF EXISTS (SELECT * 
				FROM PlaysTable AS t1 JOIN PlaysTable AS t2
				ON t1.TableID = t2.TableID AND t1.PlayerName = t2.PlayerName AND t1.TeamName = t2.TeamName
                WHERE t1.Seat != t2.Seat AND t1.PlayerName = NewPlayer AND t1.TeamName = TeamNameIn) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Repeated player at table';
	END IF;
END$$
SET DELIMITER ;