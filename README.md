## Quick Instructions

1. Clone this repository, or save `address_filterer.py` as a file on your computer.
2. Confirm that you have [Python 2.7](http://www.python.org/download/releases/2.7.2/) installed.
    * If you don't know which version to pick, choose an 'x86 installer' version for your OS from the 'downloads' section.
    * Windows users: you might need to [add it to your PATH](http://superuser.com/a/143121/132491).
3. Organize the data that needs filtering:
    1. Files must be in [CSV format](http://en.wikipedia.org/wiki/Comma-separated_values).
    2. Files must contain the same exact column headers.
4. Make a folder named `data` in the same directory as `address_filterer.py`. Place organized data files in it.
5. From a command shell, navigate to the script's folder and issue this command:  
    `python address_filterer.py`

*See the section title 'Usage' for more detailed instructions.*

## About

My boss asked me to handle the organization of our mailing list for our catalog, so I wrote this script to parse our many files full of dozens of thousands of addresses.

Several problems arise in such an exersize. Our addresses weren't organized into a single file, and so many of the addresses existed in multiple different files. Because we plan to mail out a catalog to each customer, creating and sending duplicates gets expensive fast. Anyone who has tried to solve the mathematical problem of removing duplicate entries from a collection of things can tell you that it is no small task. In most cases, especially in the context of mailing addresses, defining what constitutes a duplicate is quite diffuclt as well. Even worse is the fact that some addresses are too malformed to use in the postal system, usually due to human error such as typos, and so they must be omitted entirely from the output.

Ideally, we want a set rather than a collection. In math, a set of things is "a well defined collection", according to Wikipedia. Similarly in Python, a 'set' object is a collection that contains no duplicate elements, but, ironically, using Python's set() function is not a very efficient way to accomplish my task, I found.

After solving the problems before me and meeting my script's goals, I was able to filter about 20,000 invalid or duplicate addresses from our 64,000 total and printed them to a file in about 1 or 2 seconds with C Python 2.7.2.

Feel free to contribute to or fork this repository, but for now I am finished with this project.

### The Bottom Line:

* Saved 31% overall. In other words, we only paid 69% of what it would have cost.
* Saved $3,609 in postage costs.
* Saved $6,916 in printing costs.

### Dependencies

The script only depends on the csv and glob modules, which are included in Python's main library. It should work on any Windows box, but it may need modification to the filepath strings to work on \*nix machines.

## Usage

To properly use this script, you must first organize your data. Make a folder named `data` within the root folder and put your \*.csv data files into it.

Organize the data in your files such that the first row contains the column headers (the names of the fields of data). As this program creates a single output file, all your data/\*.csv files should contain the same exact column headers. The left-to-right order of the data columns within your files does not matter.

Finally, you may want to edit the script's main method, if you would like to customize what quantifies an invalid or duplicate address. Change the second arguments of the without_invalid and without_duplicates functions to the data column headers of your choosing. The defaults are what worked for the company I wrote this for.

Once you've done that, open a terminal and run the script like so:
    `$ python2.7 address_filterer.py`

## TODO

Create and add some sample input files for demonstration purposes.
