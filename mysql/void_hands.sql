--List boards where any hand had no cards of a given suit
SELECT DISTINCT BoardID
FROM bridgedb.hands
WHERE Hearts = '' OR Spades = '' OR Diamonds = '' OR Clubs = '';