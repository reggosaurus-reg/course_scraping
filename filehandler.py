import pathlib

# This file contains functions for file editing.


## Functions for writing to file

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

head = lambda content: "\n<head>\n<link rel=\"stylesheet\" href=\"style.css\">\n %s </head>\n" % content
body = lambda content: "\n<body>\n %s </body>\n" % content
title = lambda content: "<title> %s </title>\n" % content
heading = lambda content: "<h1> %s </h1>\n" % content
paragraph = lambda content: "<p> %s </p>\n" % content
row = lambda content: "<tr> %s </tr>\n" % content
header = lambda content: "<th> %s </th>\n" % content
data_left = lambda content: "<td class=\"data_left\"> %s </td>\n" % content
data = lambda content: "<td> %s </td>\n" % content
hyperlink = lambda content, url: "<a href= \"%s\"> %s </a>\n" % (url, content)
script = lambda type_, src: "<script type= \"%s\" src=\"%s\"></script>\n" % (type_, src)


def dotlist(data):
    """ Creates an unordered html list with dots as markers. """
    res = "<ul>\n"
    for elem in data:
        res += "<li>" + str(elem) + "</li>\n"
    return res + "\n</ul>"


## Functions for encapsulating content in correct csv syntax

def comma_to_csv(data):
    """ Takes data as a list or a string and encapsulates it in 
    a string on form "elem1, elem2..." 
    i.e. csv data element with comma. 
    """
    if isinstance(data, str):
        if "," in data:
            return "\"" + data + "\""
        else:
            return data

    if len(data) == 1:
        data = data[0]
    else:
        data = "\"" + ', '.join(data) + "\"" 
    return data 
