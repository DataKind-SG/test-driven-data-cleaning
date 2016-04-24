# test-driven-data-cleaning

Scaffold out methods and tests for collaborative data cleaning.

# Usage:
Once you clone the repo, to try it out on a very small included dataset, you can run:
```python tddc.py summarize input/foobar_data.csv```

This takes the csv data set and summarizes it, outputing to a json file in a newly created output/ directory.

Next, you can run:
```python tddc.py build_trello input/foobar_data.csv```
The first time you run this, it will fail and give you instructions on how to create a Trello configuration file in your root directory (in future, this should probably be created through the CLI).
Once you create it, you can try to run that step again. This will create a Trello board. The one my run created is here: https://trello.com/b/1mFkX6dA/data-cleaning-board-for-foobar-data

Finally, you can run:
```python tddc.py build input/foobar_data.csv```
This outputs a script into the output/ folder that contains method stubs and glue code to clean the data set. It also outputs stubs for tests in output/tests.


# TO DO:

1. allow creation of Trello credentials through CLI
2. more complete testing
3. travis
4. coveralls
5. allow user to skip Trello step
6. other integrations besides Trello?
7. allow other formats besides CSV
8. better readme (explanation for how this should be used by team leads and team members).
9. better sample dataset
10. packaging 
11. ...