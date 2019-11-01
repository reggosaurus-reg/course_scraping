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
row = lambda content: "<tr>" + content + "</tr>\n"
header = lambda content: "<th>" + content + "</th>\n"
data = lambda content: "<td>" + content + "</td>\n"
hyperlink = lambda content, url: "<a href= \"" + url + "\">" + content + "</a>\n"

def dotlist(data):
    """ Creates an unordered html list with dots as markers. """
    res = "<ul>\n"
    for elem in data:
        res += "<li>" + str(elem) + "</li>\n"
    return res + "\n</ul>"

def table(collection):
    """ Creates an html table with header and content according 
    to CourseCollection collection.
    """
    res = "<table>\n"
    heads = ""
    for h in collection.headers:
        heads += header(h)
    res += row(heads)
    
    for course in collection:
        data_row = ""
        data_row += data(course.code)
        data_row += data(hyperlink(course.name, course.url))
        data_row += data(course.level)
        data_row += data(course.points)
        data_row += data(course.period)
        data_row += data(course.block)
        res += row(data_row)

    res += "</table>\n"
    return res
