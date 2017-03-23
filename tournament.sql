-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

CREATE TABLE player_registration (ID SERIAL primary key,
                                  Name TEXT);

CREATE TABLE matches (Match_Number SERIAL primary key,
                      Winner INTEGER references player_registration (ID),
                      Loser INTEGER references player_registration (ID))
