#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDeleteTournamentPlayers():
    deleteMatches()
    deleteTournamentPlayers()
    print "2. Old tournamentPlayers can be deleted."


def testDelete():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()
    print "3. Player & tournament records can be deleted."


def testCount():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()

    # Count all players
    c = countPlayers(0)

    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "4. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()

    # Register a tournament
    tournamentId = registerTournament("Kabaddi Tourney")
    # Register a player 
    playerId = registerPlayer("Chandra Nalaar")
    # Add player to the above tournament
    registerTournamentPlayer(tournamentId, playerId)

    # Count the players registered to the above tournament
    c = countPlayers(tournamentId)

    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "5. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()

    # Register a tournament
    tournamentId = registerTournament("A Chess Event")
    # Register four player
    playerId1 = registerPlayer("Markov Chaney")
    playerId2 = registerPlayer("Joe Malik")
    playerId3 = registerPlayer("Mao Tsu-hsi")
    playerId4 = registerPlayer("Atlanta Hope")
    # Add players 1 to 4 to the tournament 
    registerTournamentPlayer(tournamentId, playerId1)
    registerTournamentPlayer(tournamentId, playerId2)
    registerTournamentPlayer(tournamentId, playerId3)
    registerTournamentPlayer(tournamentId, playerId4)

    # Count the players registered to the above tournament
    c = countPlayers(tournamentId)

    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")

    deleteTournamentPlayers()
    deletePlayers()

    # Count all players
    c = countPlayers(0)

    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "6. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()

    # Register a tournament
    tournamentId = registerTournament("Scrabble Rabble")
    # Register two players
    playerId1 = registerPlayer("Melpomene Murray")
    playerId2 = registerPlayer("Randy Schwartz")
    # Add the players to the tournament
    registerTournamentPlayer(tournamentId, playerId1)
    registerTournamentPlayer(tournamentId, playerId2)

    standings = playerStandings(tournamentId)

    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()

    # Register two tournaments
    tournamentId1 = registerTournament("Ludo Love In")
    tournamentId2 = registerTournament("Draughts Laughs")
    # Register four players
    playerId1 = registerPlayer("Bruno Walton")
    playerId2 = registerPlayer("Boots O'Neal")
    playerId3 = registerPlayer("Cathy Burton")
    playerId4 = registerPlayer("Diane Grant")
    # Add players 1 to 4 to tournament 1  
    registerTournamentPlayer(tournamentId1, playerId1)
    registerTournamentPlayer(tournamentId1, playerId2)
    registerTournamentPlayer(tournamentId1, playerId3)
    registerTournamentPlayer(tournamentId1, playerId4)
    # Add players 1 & 3 to tournament 2
    registerTournamentPlayer(tournamentId2, playerId1)
    registerTournamentPlayer(tournamentId2, playerId3)

    # Return player standings for tournament 1
    standings = playerStandings(tournamentId1)
    [id1, id2, id3, id4] = [row[0] for row in standings]

    # Add first round match results, including games won/lost, to tournament 1 
    reportMatch(tournamentId1, id1, id2, 3, 1)
    reportMatch(tournamentId1, id3, id4, 3, 2)

    # Return player standings for tournament 1
    standings = playerStandings(tournamentId1)

    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "8. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    deleteTournaments()

    # Register two tournaments
    tournamentId1 = registerTournament("Pool Shark Park")
    tournamentId2 = registerTournament("Tennis Menace")
    # Register four players
    playerId1 = registerPlayer("Twilight Sparkle")
    playerId2 = registerPlayer("Fluttershy")
    playerId3 = registerPlayer("Applejack")
    playerId4 = registerPlayer("Pinkie Pie")
    # Add players 1 to 4 to tournament 1  
    registerTournamentPlayer(tournamentId1, playerId1)
    registerTournamentPlayer(tournamentId1, playerId2)
    registerTournamentPlayer(tournamentId1, playerId3)
    registerTournamentPlayer(tournamentId1, playerId4)
    # Add players 1 & 3 to tournament 2
    registerTournamentPlayer(tournamentId2, playerId1)
    registerTournamentPlayer(tournamentId2, playerId3)
    
    # Return player standings for tournament 1
    standings = playerStandings(tournamentId1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    
    # Add first round match results, including games won/lost, to tournament 1 
    reportMatch(tournamentId1, id1, id2, 5, 4)
    reportMatch(tournamentId1, id3, id4, 5, 2)
    
    # Return pairings after first round results
    pairings = swissPairings(tournamentId1)
    # Note, would check here for odd number of players return (0, '', 0, '')

    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    
    # Add 2nd Round results
    reportMatch(tournamentId1, pid1, pid2, 5, 2)
    reportMatch(tournamentId1, pid3, pid4, 5, 3)
    
    # Return pairings after first round results
    pairings = swissPairings(tournamentId1)
    # Note, would check here for odd number of players return (0, '', 0, '')
    
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id2]), frozenset([id3, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After two matches, player with two wins should be paired to best player with one win.")
    
    print "9. After one match, players with one win are paired."
    print "   After two matches, player with two wins is paired to best player with one win"


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"


