.. image:: https://travis-ci.org/DataKind-SG/test-driven-data-cleaning.svg?branch=master
    :target: https://travis-ci.org/DataKind-SG/test-driven-data-cleaning# Test Driven Data Cleaning
    :alt: Build Status

Scaffold out methods and tests for collaborative data cleaning.

======
Usage:
======

This works on Linux with Python 2.7, 3.3, 3.4 and 3.5, and on OSX with Python 2.7 and 3.5 (and probably 3.3 and 3.4, but that hasn't been tested. It may work on Windows (but probably not).

Install the package with:
``$ pip install tddc``

You can download a tiny example CSV file at: https://github.com/DataKind-SG/test-driven-data-cleaning/raw/master/input/foobar_data.csv

In the same directory as the file, run:

``$ tddc summarize foobar_data.csv``

This takes the csv data set and summarizes it, outputing to a json file in a newly created output/ directory.

Next, you can run:

``$ tddc build_trello foobar_data.csv``

The first time you run this, it will fail and give you instructions on how to create a Trello configuration file in your root directory (in future, this should probably be created through the CLI).
Once you create it, you can try to run that step again. This will create a Trello board. The one my run created is here: https://trello.com/b/cqP9VZal/data-cleaning-board-for-foobar-data 

Finally, you can run:

``$ tddc build foobar_data.csv``

This outputs a script into the output/ folder that contains method stubs and glue code to clean the data set. It also outputs stubs for tests in output/.

Running tests
=============

You can run the tests with 

``$ py.test``

in the root of the project directory.


TO DO:
======

1. allow creation of Trello credentials through CLI
2. more complete testing
3. travis [COMPLETE]
4. coveralls
5. allow user to skip Trello step
6. other integrations besides Trello?
7. allow other formats besides CSV
8. better readme (explanation for how this should be used by team leads and team members).
9. better sample dataset
10. packaging [COMPLETE]
11. export to Jupyter notebook
12. ...
