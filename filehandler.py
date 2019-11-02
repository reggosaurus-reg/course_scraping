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


def write(content, filename, content_type, unsafe=False):
    """ If safe, writes content to the file filename. 
    Writes a result message containing content_type. """
    if unsafe or safe_to_write(filename):
        with open(filename, 'w') as f:
            f.write(content)
        print("""Wrote resulting %s to '%s'.\n""" % (content_type, filename))
    else:
        print("Aborting %s write operation.\n" % content_type)


## Functions for encapsulating content in correct html syntax
head = lambda content: "\n<head>\n<link rel=\"stylesheet\" href=\"style.css\">\n" + content + "</head>\n"
body = lambda content: "\n<body>\n" + content + "</body>\n"
title = lambda content: "<title>" + content + "</title>\n"
heading = lambda content: "<h1>" + content + "</h1>\n"
paragraph = lambda content: "<p>" + content + "</p>\n"
row = lambda content: "<tr>" + content + "</tr>\n"
header = lambda content: "<th>" + content + "</th>\n"
data_left = lambda content: "<td class=\"data_left\">" + content + "</td>\n"
data = lambda content: "<td>" + content + "</td>\n"
hyperlink = lambda content, url: "<a href= \"" + url + "\">" + content + "</a>\n"

def dotlist(data):
    """ Creates an unordered html list with dots as markers. """
    res = "<ul>\n"
    for elem in data:
        res += "<li>" + str(elem) + "</li>\n"
    return res + "\n</ul>"

