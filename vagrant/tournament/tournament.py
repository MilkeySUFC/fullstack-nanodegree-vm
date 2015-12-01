#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conTournament = connect()

    curMatchesDel = conTournament.cursor()
    curMatchesDel.execute("DELETE FROM matches")

    conTournament.commit()

    conTournament.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conTournament = connect()

    curPlayersDel = conTournament.cursor()
    curPlayersDel.execute("DELETE FROM players")

    conTournament.commit()

    conTournament.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conTournament = connect()

    curPlayersCount = conTournament.cursor()
    curPlayersCount.execute("SELECT COUNT(*) AS PlayerCount FROM players")

    playerCount = curPlayersCount.fetchone()

    conTournament.close()

    return playerCount[0]

def registerPlayer(name, dob):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      dob: the player's date of birth (need not be unique).
    """
    conTournament = connect()

    curPlayerReg = conTournament.cursor()
    curPlayerReg.execute("INSERT INTO players (name, dob) VALUES (%s, %s)", (bleach.clean(name), bleach.clean(dob)))

    conTournament.commit()
    conTournament.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conTournament = connect()

    curPlayerStandings = conTournament.cursor()
    curPlayerStandings.execute("SELECT id, name, wins, matches FROM standings")

    player_Standings = curPlayerStandings.fetchall()

    conTournament.close()

    return player_Standings


def reportMatch(winnerId, loserId, winnerGames, loserGames):
    """Records the outcome of a single match between two players.

    Args:
      winnerId:  the id number of the player who won
      loserId:  the id number of the player who lost
      winnerGames:  the number of games the winning player won
      loserGames:  the number of games the losing player lost
    """
    conTournament = connect()

    curMatchRep = conTournament.cursor()
    curMatchRep.execute("INSERT INTO matches (winnerId, loserId, winnerGames, loserGames) VALUES (%s, %s, %s, %s)", 
        (bleach.clean(winnerId), bleach.clean(loserId), bleach.clean(winnerGames), bleach.clean(loserGames)))

    conTournament.commit()
    conTournament.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conTournament = connect()

    curPairings = conTournament.cursor()
    curPairings.execute("SELECT id1, name1, id2, name2 FROM fnPairings()")

    pairings = curPairings.fetchall()

    conTournament.close()

    return pairings


