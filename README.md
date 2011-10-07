About
-----

My boss asked me to handle the mailing list of our catalog, so I wrote this script to filter through our many files full of dozens of thousands of addresses. They weren't organized into a single file, and so many of the addresses of our customers existed in multiple different files. Because we plan to mail out a catalog to each customer, sending duplicates gets expensive fast.

This script filtered about 20,000 invalid or duplicate addresses from our 64,000 total, and printed them to a file, in about 1 or 2 seconds with C Python 2.7.2.

It only depends on the csv and glob modules, which are included in Python's main library. csv_filterer.py should work on any Windows box, but it may need modification to the filepath strings to work on *nix machines. Test that for me and submit a bug report so that I can fix it for you!

Feel free to contribute to or fork this repository, but for now I am finished with this project.

Usage
-----

To properly use this script, you must first organize your data. Make a folder named 'data' folder within the csv_filterer folder and put your *.csv files into it.

Organize the data in your files such that the first line contains the column headers (the names of the fields of data). As this program creates a single output file, all your data/*.csv files should contain the same exact column headers. The left-to-right order of the data columns within your files does not matter.

Finally, you'll want to edit the script's main method. Change the second arguments of the without_invalid and without_duplicates functions to the data column headers of your choosing.

TODO
----

Create and add some sample input files for demonstration purposes.
