import pathlib

# This file contains functions for file editing.


def safe_to_write(filename):
    """ Warn the user if file exists and prompts to be sure to overwrite.
    Otherwise returns that it is safe to write. 
    """
    if pathlib.Path(filename).exists():
        print("""The file '%s' already exists. 
                \rDo you wish to overwrite it? (y/N) """ % filename)
        return str(input()) == "y"
    return True


## Functions for encapsulating content in correct html syntax
head = lambda content: "\n<head>\n" + content + "</head>\n"
body = lambda content: "\n<body>\n" + content + "</body>\n"
title = lambda content: "<title>" + content + "</title>\n"
heading = lambda content: "<h1>" + content + "</h1>\n"
paragraph = lambda content: "<p>" + content + "</p>\n"

def dotlist(iterable):
    """ Creates an unordered html list with dots as markers. """
    res = "<ul>\n"
    for elem in iterable:
        res += "<li>" + str(elem) + "</li>"
    return res + "\n</ul>"
