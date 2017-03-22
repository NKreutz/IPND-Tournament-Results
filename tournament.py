#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    c.execute("UPDATE player_registration set wins = 0")
    c.execute("UPDATE player_registration set matches = 0")
    DB.commit()
    DB.close


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player_registration")
    DB.commit()
    DB.close

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) as num FROM player_registration")
    results = c.fetchall()
    number_of_players = results[0][0]
    DB.close
    return number_of_players

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    SQL = "INSERT INTO player_registration (name, wins, matches) VALUES (%s, 0, 0);"
    data = (name, )
    c.execute(SQL, data)
    DB.commit()
    DB.close()

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
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM player_registration ORDER BY Wins DESC")
    standings = c.fetchall()
    DB.close
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    SQL = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser, )
    c.execute(SQL, data)
    SQL2 = "UPDATE player_registration set matches = (matches + 1) where ID = (%s) or ID = (%s);"
    c.execute(SQL2, data)
    SQL3 = "UPDATE player_registration set wins = (wins + 1) where ID = (%s);"
    data2 = (winner, )
    c.execute(SQL3, data2)
    DB.commit()
    DB.close()

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
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT ID, Name FROM player_registration ORDER BY Wins DESC")
    number_of_pairs = countPlayers() / 2
    pairs = []
    for pair in range(number_of_pairs):
        results = c.fetchmany(2)
        [id1, id2] = [row[0] for row in results]
        [name1, name2] = [row[1] for row in results]
        pairs.append((id1, name1, id2, name2))
    DB.close
    return pairs
