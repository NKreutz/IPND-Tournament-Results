-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE player_registration (ID SERIAL primary key,
                                  Name TEXT,
                                  Wins INTEGER,
                                  Matches INTEGER);

CREATE TABLE matches (Winner INTEGER references player_registration (ID),
                      Loser INTEGER references player_registration (ID))
