This package provides code examples for the file iterator package.

The ```circles_file_iterator``` package provides classes and utility functions for handling file interactions with CIRCLES CyVerse.

It allows:
- Communication with CyVerse's fileshare (ls, cd, pwd)
- I/O Commands through IRODS
- Iterating over files from CyVerse
- Cache handling

# Installation
To install the packages needed, simply run:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, you can configure the file iterator by runnning the following command:
```
python3 -m circles_file_iterator
```
It will ask for some information, fill it out and it should be fine

*WARNING:* If you use a different name for your virtual environment, the ```__main__.py``` script from circles_file_iterator might not work.
*WARNING 2:* Run those commands from the folder's base (here, from ```/file_iterator_code_examples/```).


# Code examples

Several file examples are available for you to try the functionnalities provided by this package.

The commands' usage is describe in the comments of the code examples files.

The output of those file when you run them shows the results of the different actions launched.

To run a code example, simply run the following command in a terminal (from the folder root, with the virtual environment activated):
```
python3 example_name.py
```


# Useful Links

*GitHub repository of the circles_file_iterator package:* https://github.com/codingrosquick
*PyPI page of the circles_file_iterator package:* https://pypi.org/project/circles-file-iterator/
