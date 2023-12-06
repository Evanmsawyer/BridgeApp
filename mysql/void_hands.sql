--List boards where any hand had no cards of a given suit
SET DELIMITER $$
CREATE PROCEDURE VoidHandSearch() 
BEGIN
    SELECT *
    FROM BridsgeDB.Hands
    WHERE Hearts = '' OR Spades = '' OR Diamonds = '' OR Clubs = '';
END$$
SET DELIMITER ;