#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """ Connect to the PostgreSQL tournament database.  
        Returns a database connection and cursor object."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unable to connect to database/create cursor")

def deleteTournaments():
    """Remove all the tournament records from the database."""
    conTournament, curTournament  = connect()

    curTournament.execute("DELETE FROM tournaments")

    conTournament.commit()

    conTournament.close()


def deleteTournamentPlayers():
    """Remove all the tournamentPlayer records from the database."""
    conTournament, curTournamentPlayersDel = connect()

    curTournamentPlayersDel.execute("DELETE FROM tournamentPlayers")

    conTournament.commit()

    conTournament.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conTournament, curMatchesDel = connect()

    curMatchesDel.execute("DELETE FROM matches")

    conTournament.commit()

    conTournament.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conTournament, curPlayersDel = connect()

    curPlayersDel.execute("DELETE FROM players")

    conTournament.commit()

    conTournament.close()


def countPlayers(tournamentId):
    """Returns the number of players currently registered.

    Args:
        tournamentId:   tournamentId of the tournament to count players registered to.
                        0 to count all players or Id of tournament to count 
    """
    conTournament, curPlayersCount = connect()

    # Check if counting all tournaments or specific tournaments
    if tournamentId == 0:
        curPlayersCount.execute("SELECT COUNT(*) AS PlayerCount FROM players")
    elif tournamentId != 0:
        curPlayersCount.execute("SELECT COUNT(*) AS PlayerCount FROM tournamentPlayers WHERE tournamentId = %s", (bleach.clean(tournamentId), ))

    playerCount = curPlayersCount.fetchone()

    conTournament.close()

    return playerCount[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conTournament, curPlayerReg = connect()

    curPlayerReg.execute("INSERT INTO players (name) VALUES (%s) RETURNING id", (bleach.clean(name), ))

    playerId = curPlayerReg.fetchone()

    conTournament.commit()
    conTournament.close()

    return playerId[0]

def registerTournament(name):
    """Adds a tournament to the tournament database.
  
    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      tournament: the tournament's full name (need not be unique).
    """
    conTournament, curTournamentReg  = connect()

    curTournamentReg.execute("INSERT INTO tournaments (name) VALUES (%s) RETURNING id", (bleach.clean(name), ))

    tournamentId = curTournamentReg.fetchone()

    conTournament.commit()
    conTournament.close()

    return tournamentId[0]

def registerTournamentPlayer(tournamentId, playerId):
    """Adds a tournamentPlayer record to the tournament database.
  
    Args:
      tournamentId: the tournamentId to add
      playerId: the playerId to add
    """
    conTournament, curTournamentPlayerReg = connect()

    curTournamentPlayerReg.execute("INSERT INTO tournamentPlayers (tournamentId, playerId) VALUES (%s, %s)", (bleach.clean(tournamentId), bleach.clean(playerId)))

    conTournament.commit()
    conTournament.close()


def playerStandings(tournamentId):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
  
    Args:
      tournamentId: the tournamentId to return the standings for
    """
    conTournament, curPlayerStandings = connect()

    curPlayerStandings.execute("SELECT id, name, wins, matches FROM standings WHERE tournamentId = %s", (bleach.clean(tournamentId), ))

    player_Standings = curPlayerStandings.fetchall()

    conTournament.close()

    return player_Standings


def reportMatch(tournamentId, winnerId, loserId, winnerGames, loserGames):
    """Records the outcome of a single match between two players.

    Args:
      tournamentId: the id number of the tournament to record a match for
      winnerId:  the id number of the player who won
      loserId:  the id number of the player who lost
      winnerGames:  the number of games the winning player won
      loserGames:  the number of games the losing player lost
    """
    conTournament, curMatchRep = connect()

    curMatchRep.execute("INSERT INTO matches (tournamentId, winnerId, loserId, winnerGames, loserGames) VALUES (%s, %s, %s, %s, %s)", 
        (bleach.clean(tournamentId), bleach.clean(winnerId), bleach.clean(loserId), bleach.clean(winnerGames), bleach.clean(loserGames)))

    conTournament.commit()
    conTournament.close()
 
 
def swissPairings(tournamentId):
    """Returns a list of pairs of players for the next round of a match, for the given tournament Id.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournamentId: the id number of the tournament to return pairings for 

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conTournament, curPairings = connect()

    curPairings.execute("SELECT id1, name1, id2, name2 FROM fnPairings(%s)", (bleach.clean(tournamentId), ))

    pairings = curPairings.fetchall()

    conTournament.close()

    return pairings


