SET DELIMITER $$
CREATE PROCEDURE SuitSearch(SpadesInput INT, HeartsInput INT, DiamondsInput INT, ClubsInput INT)
BEGIN
    SELECT * 
    FROM bridgedb.Hands 
    WHERE LENGTH(Spades) = SpadesInput AND LENGTH(Hearts) = HeartsInput AND LENGTH(Diamonds) = DiamondsInput AND LENGTH(Clubs) = ClubsInput;
END$$
SET DELIMITER ;
