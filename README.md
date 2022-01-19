# Data Pipeline Submission for Tagup Skills Test

## Summary
I have provided two files for this submission.

1. `pipeline.ipynb` which contains Markdown cells explaining my choices and decision making, as well as some simple visualizations. This is the file that I primarily worked from while completing the assignment.

2. `pipeline.py`, which removes the Markdown cells and visualizations, and refactors much of the code to be more readable, extensible and more in line with object-oriented design.

Both of these files accomplish the same goal (minus the .py file which does not produce visualizations), which is to load the four data tables from `exampleco_db.db` into a Pandas DataFrame, clean the data, and finally reshape the data into an xarray DataArray with labeled dimensions and coordinates.

The decision to load the data before transforming it was made primarily because of its relatively small size (about 26 MB). Loading the data before transforming it allows us to inspect the data intermittently as we make changes to it, without having to wait for a response from the database.