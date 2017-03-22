## Swiss Style Tournament Application
**Project Submission for Udacity's Intro to Programming Nanodegree**

This project is an application that records player standings and creates player pairings for each round in a [swiss-style tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament).

### Dependencies

This project is written in Python and uses the PostgreSQL Database on a [Vagrant](https://www.vagrantup.com/)/[Virtualbox](https://www.virtualbox.org/wiki/Downloads) based Virtual Machine.

### Installation/ Quick Start

1. Install Vagrant and VirtualBox
* Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository
* Replace the Tournament folder in the fullstack-nanodegree-vm repository with this [repository](https://github.com/NKreutz/IPND-Tournament-Results.git)
* Launch the Vagrant VM
    * Using the terminal (on Mac), `cd` into the Vagrant folder
    * Run the command `vagrant up`
    * Run the command `vagrant ssh`
* `cd` into tournament folder
* Run the test suite to verify code using `python tournament_test.py`

### Usage

To run a Swiss-style tournament:

1. Create a new .py file in the tournament folder
* Run `from tournament import *`
* Run `deleteMatches()` and `deletePlayers()` to clear the player board
* Register players in your tournament using `registerPlayer(name)`
* Print `swissPairings()` to receive a list of pairings for the next round.
* Record match results using `reportMatch(winner, loser)` (using unique ID, not the player's name)
* Print `playerStandings()` to receive a list of current player standings
* Repeat steps 5 through 7 as needed
* Run `deleteMatches()` and `deletePlayers()` to clear the player board for the next tournament

### Credits

This project is based off of starter code obtained via [Udacity's](https://www.udacity.com/) Intro to Programming Nanodegree in March 2017, and has been modified by Narissa Kreutz.
