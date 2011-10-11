About
-----

My boss asked me to handle the organization of our mailing list for our catalog, so I wrote this script to parse our many files full of dozens of thousands of addresses.
 
Several problems arise in such an exersize. Our addresses weren't organized into a single file, and so many of the addresses existed in multiple different files. Because we plan to mail out a catalog to each customer, creating and sending duplicates gets expensive fast. Anyone who has tried to solve the mathematical problem of removing duplicate entries from a collection of things can tell you that it is no small task. In most cases, especially in the context of mailing addresses, defining what constitutes a duplicate is quite diffuclt as well. Even worse is the fact that some addresses are too malformed to use in the postal system, usually due to human error such as typos, and so they must be omitted entirely from the output.

Ideally, we want a set rather than a collection. In math, a set of things is "a well defined collection", according to Wikipedia. Similarly in Python, a 'set' object is a collection that contains no duplicate elements, and so that is the definition I will use as well. Ironically, using Python's set() function is not a very efficient or comprehensive way to accomplish my task, I found.

After solving the problems before me and meeting my script's goals, I was able to filter about 20,000 invalid or duplicate addresses from our 64,000 total and printed them to a file in about 1 or 2 seconds with C Python 2.7.2.

The script only depends on the csv and glob modules, which are included in Python's main library. It should work on any Windows box, but it may need modification to the filepath strings to work on *nix machines.

Feel free to contribute to or fork this repository, but for now I am finished with this project.

Usage
-----

To properly use this script, you must first organize your data. Make a folder named 'data' folder within the repo's root folder and put your *.csv files into it.

Organize the data in your files such that the first line contains the column headers (the names of the fields of data). As this program creates a single output file, all your data/*.csv files should contain the same exact column headers. The left-to-right order of the data columns within your files does not matter.

Finally, you may want to edit the script's main method, if you would like to customize what quantifies an invalid or duplicate address. Change the second arguments of the without_invalid and without_duplicates functions to the data column headers of your choosing.

For an example of properly formatted input data, view the example csv file. # Not yet implemented.

TODO
----

Create and add some sample input files for demonstration purposes.
