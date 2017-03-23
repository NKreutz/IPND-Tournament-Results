#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error connecting to Database")


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE matches")
    DB.commit()
    DB.close


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE player_registration CASCADE")
    DB.commit()
    DB.close


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("SELECT count(*) as num FROM player_registration")
    results = c.fetchone()
    number_of_players = results[0]
    DB.close
    return number_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    SQL = "INSERT INTO player_registration (name) VALUES (%s);"
    data = (name, )
    c.execute(SQL, data)
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    c.execute('''SELECT player_registration.ID, player_registration.Name,
                COUNT(matches.winner) as Wins
                FROM player_registration
                LEFT JOIN matches
                ON player_registration.ID=matches.winner
                GROUP BY player_registration.ID
                ORDER BY Wins DESC''')
    players = c.fetchall()
    standings = []
    for row in players:
        id, name, wins = row[0], row[1], row[2]
        c.execute('''SELECT COUNT(*) AS Matches_Played
                    FROM matches
                    WHERE Winner = %s OR Loser = %s ''', (id, id, ))
        matches_played = c.fetchone()[0]
        standings.append((id, name, wins, matches_played))
    DB.close
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    SQL = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser, )
    c.execute(SQL, data)
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
    number_of_pairs = countPlayers() / 2
    pairs = []
    slice = 0
    for pair in range(number_of_pairs):
        results = playerStandings()
        [id1, id2] = [row[0] for row in results[slice:(slice + 2)]]
        [name1, name2] = [row[1] for row in results[slice:(slice + 2)]]
        pairs.append((id1, name1, id2, name2))
        slice += 2
    return pairs
