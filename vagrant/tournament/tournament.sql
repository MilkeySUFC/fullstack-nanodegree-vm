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

DROP TABLE IF EXISTS tournaments;

CREATE TABLE tournaments (
	id SERIAL,
	name TEXT,
	PRIMARY KEY (id)
	);

DROP TABLE IF EXISTS players;

CREATE TABLE players (
	id SERIAL,
	name TEXT,
	PRIMARY KEY (id)
	);

DROP TABLE IF EXISTS tournamentPlayers;

CREATE TABLE tournamentPlayers (
	tournamentId INTEGER REFERENCES tournaments (id),
	playerId INTEGER REFERENCES players (id),
	PRIMARY KEY (tournamentId, playerId)
	);

DROP TABLE IF EXISTS matches;

CREATE TABLE matches (
	id SERIAL ,
	tournamentId INTEGER,
	winnerId INTEGER,
	loserId INTEGER,
	winnerGames INTEGER,
	loserGames INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (tournamentId, winnerId) REFERENCES tournamentPlayers (tournamentId, playerId),
	FOREIGN KEY (tournamentId, loserId) REFERENCES tournamentPlayers (tournamentId, playerId)
	);

DROP VIEW IF EXISTS standings;

CREATE VIEW standings AS
--	View to return the current standings for all players, for all tournaments that have players assigned
--	Sorted by:
--		tournamentId (ascending)
--		number of wins (descending)
--		number of games won (descending)
--		number of matches played (ascending)
	SELECT 	tTP.tournamentId,
			tP.id, 
			tP.name, 
			COUNT(tW.winnerId) AS wins, 
			COUNT(tW.tournamentId) + COUNT(tL.tournamentId) AS matches,
			SUM(COALESCE(tW.winnerGames,0) + COALESCE(tL.loserGames,0)) AS gamesWon,
			SUM(COALESCE(tW.loserGames,0) + COALESCE(tL.winnerGames,0)) AS gamesLost
	FROM 	(tournamentPlayers tTP
			LEFT JOIN 	players tP
						ON 	tTP.playerId = tP.id
			)
			LEFT JOIN 	matches tW 	-- Matches, joined by winnerId
						ON 	tTP.tournamentId = tW.tournamentId
						AND tP.id = tW.winnerId 
			LEFT JOIN 	matches tL 	-- Matches, joined by loserId
						ON 	tTP.tournamentId = tL.tournamentId
						AND tP.id = tL.loserId
	GROUP BY tTP.tournamentId,
			tP.id, 
			tP.name
	ORDER BY tournamentId ASC,
			wins DESC,
			gamesWon DESC,
			matches ASC ;

DROP FUNCTION IF EXISTS fnPairings();

CREATE FUNCTION fnPairings(intTournamentId INTEGER) 
--	Function to return the pairings as a table.
--
--	Args:
--		intTournamentId: tournamentId for which to return pairings
--
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
				FROM	standings
				WHERE	tournamentId = intTournamentId;

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
