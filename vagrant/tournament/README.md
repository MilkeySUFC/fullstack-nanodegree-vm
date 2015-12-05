
# Full-Stack Web Developer NanoDegree

## Project 2. Tournament Database

### Installation

Refer to installation notes in the Full-Stack Web Developer NanoDegree for setting up VirtualBox & Vagrant.

### Set-Up

SSH into the vagrant VM.

Change to the tournament directory: 

	`cd /vagrant/tournament/`

To build the _tournament_ database, run the PostgresSQL shell:

	`psql'

and, from the psql shell, import/run the tournament database setup sql:

	`\i tournament.sql;`

### Running the tests

Run the test file using the command:

	`python tournament_test.py`
