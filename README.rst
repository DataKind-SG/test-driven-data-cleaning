.. image:: https://travis-ci.org/DataKind-SG/test-driven-data-cleaning.svg?branch=master
    :target: https://travis-ci.org/DataKind-SG/test-driven-data-cleaning# Test Driven Data Cleaning
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/DataKind-SG/test-driven-data-cleaning/badge.svg?branch=master
    :target: https://coveralls.io/github/DataKind-SG/test-driven-data-cleaning?branch=master

This package provides a framework for collaborative, test-driven data cleaning. The framework enables a reproducible method for data cleaning that can be easily validated.

For a given tabular data set, a Trello board is populated with cards for each column so that team members can tag themselves to a column and ensure that work does not overlap. The cards include summary statistics of the columns that can be useful for writing methods to clean the column. Method stubs and test stubs are also scaffolded out for team members to fill out.

==============
Pre-requisite:
==============

You should have a Trello account. If not, you can create one at https://trello.com

======
Usage:
======

This works on Linux with Python 2.7, 3.3, 3.4 and 3.5, and on OSX with Python 2.7 and 3.5 (and probably 3.3 and 3.4, but those haven't been tested).
It works on Windows (tested using Python 3.5.2 :: Anaconda 4.1.1 (64-bit)).
Integration with Trello on Windows using tddc is yet to be tested though.

Install the package with:

``$ pip install tddc``

You can download a tiny example CSV file at: https://github.com/DataKind-SG/test-driven-data-cleaning/raw/master/input/foobar_data.csv

In the same directory as the file, run:

``$ tddc summarize foobar_data.csv``

This takes the csv data set and summarizes it, outputing to a json file in a newly created output/ directory.

If this is the first time you're running this, you should create a Trello configuration file named ``.tddc_config.yml`` in your user root directory with the format::

    trello:
        api_key: <TRELL_API_KEY>
        token: <TRELLO_TOKEN>

You can get your Trello API key here: https://trello.com/app-key

Replace your Trello API key at the end of this URL to get your Trello token::

    https://trello.com/1/authorize?expiration=1day&scope=read,write,account&response_type=token&name=Server%20Token&key=<TRELLO_API_KEY>

Next, you can run:

``$ tddc build_trello foobar_data.csv``

The first time you run this, it will fail and give you instructions on how to create a Trello configuration file in your root directory (in future, this should probably be created through the CLI).
Once you create it, you can try to run that step again. This will create a Trello board. The one my run created is here: https://trello.com/b/cqP9VZal/data-cleaning-board-for-foobar-data

Finally, you can run:

``$ tddc build foobar_data.csv``

This outputs a script into the output/ folder that contains method stubs and glue code to clean the data set. It also outputs stubs for tests in output/.

Contributing:
=============

Before running the tests, you'll need to run:

``$ pip install pytest pytest-cov mock``

Then, in the root of the project directory you can run the tests with:

``$ py.test``

We're trying out the new Github projects feature. The project we're currently working on is https://github.com/DataKind-SG/test-driven-data-cleaning/projects/1

Each card is an issue that you can click through to. If you'd like to take a card (thank you!), move the card to the "In progress" column and assign yourself to the issue. Once you're finished, issue a pull request and move the card to "For review".

If you think of a new issue, create the card in the appropriate project and convert the card to an issue in the pull-down menu (it's currently not possible to link to an already created issue from a card).
