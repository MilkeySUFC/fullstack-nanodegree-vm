-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with tWo dashes, like
-- these lines here.

\c vagrant

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS players;

CREATE TABLE players (
	id SERIAL,
	name TEXT,
	dob DATE,
	PRIMARY KEY(id)
	);

DROP TABLE IF EXISTS matches;

CREATE TABLE matches (
	id SERIAL ,
	winnerId INTEGER REFERENCES players (id),
	loserId INTEGER REFERENCES players (id),
	winnerGames INTEGER,
	loserGames INTEGER,
	PRIMARY KEY(id)
	);

DROP VIEW IF EXISTS standings;

CREATE VIEW standings AS
	SELECT 	tP.id, 
			tP.name, 
			COUNT(tW.winnerId) AS wins, 
			COUNT(tM.winnerId) AS matches,
			SUM(COALESCE(tW.winnerGames,0) + COALESCE(tL.loserGames,0)) AS gamesWon,
			SUM(COALESCE(tW.loserGames,0) + COALESCE(tL.winnerGames,0)) AS gamesLost
	FROM 	players tP 
			LEFT JOIN 	matches tM 
						ON 	tP.id = tM.winnerId 
						OR 	tP.id = tM.loserId 
			LEFT JOIN 	matches tW 
						ON 	tP.id = tW.winnerId 
			LEFT JOIN 	matches tL 
						ON 	tP.id = tL.loserId 
	GROUP BY tP.id, 
			tP.name
	ORDER BY wins DESC,
			gamesWon DESC,
			matches ASC ;

DROP FUNCTION IF EXISTS fnPairings();

CREATE FUNCTION fnPairings() 
--	Function to return the pairings as a table.
	RETURNS TABLE(
		id1 INTEGER,
		name1 TEXT,
		id2 INTEGER,
		name2 TEXT) 
	AS
$$
	BEGIN
--	Creates temp table of standings, with current rank serial ID.
--	Return query returns rows for odd ranked IDs joined to itself
--	on ID = (ID - 1), to pair it to the next even ranked player
		DROP TABLE IF EXISTS tmpStandings;

		CREATE TEMPORARY TABLE tmpStandings (
			rank SERIAL,
			standingId INTEGER
			);

		INSERT INTO tmpStandings
				(standingId)
				SELECT	id
				FROM	standings;

		RETURN QUERY
			SELECT 	tSOdd.standingId id1,
					tPOdd.name name1,
					tSEven.standingId id2,
					tPEven.name name2
			FROM	(tmpStandings tSOdd
						JOIN	players tPOdd
								ON	tSOdd.standingId = tPOdd.id)
					JOIN	(tmpStandings tSEven
								JOIN	players tPEven
									ON	tSEven.standingId = tPEven.id)
						ON tSOdd.rank = (tSEven.rank - 1)
			WHERE	tSOdd.rank % 2 = 1;


		DROP TABLE IF EXISTS tmpStandings;
	END;
$$
	LANGUAGE plpgsql;
