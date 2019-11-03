import requests
from bs4 import BeautifulSoup
from filehandler import *

# This file contains all the classes tied to representing courses.


class Course():
    """ Representation of a course. """

    def __init__(self, course, info, vtht, period_num):
        """ Takes a course tag 'course' and some info and extracts all 
        needed members.
        """
        self.code = course["data-course-code"] 
        self.name = course.a.text
        self.level = info[3]
        self.blocks = [info[4]] # List to allow several blocks 
        self.url = course.a["href"]

        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, features="html5lib") 
        self.areas =self.parse_areas(list(
            soup.find('div', attrs={'class': 'overview col-md-7'}).text.split()))

        # Handles courses spanning over several periods
        # period: VT/HT + 1, 2 or '*' (means both)
        points = info[2]
        if points[-1] == '*':
            self.points = points[:-1] 
            self.period = vtht + '*'  
        else:
            self.points = points
            self.period = vtht + period_num

    def parse_areas(self, seq):
        """ Returns a new list with all area pieces from seq as coherent
        separate elements. 
        """
        res = []
        area = ""
        for elem in seq[1:]:
            # Capital letter = new area
            if elem[0].isupper():
                # Save old area
                if area:
                    res.append(area)
                area = elem
            # Continue parsing new area
            else:
                area += " " + elem

        res.append(area)
        return sorted(res)

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        """ Prints the course. """ 
        points = self.points
        points = points + ')' if len(points) == 2 else points + ') ' 
        return '[' + self.period + '] ' + \
                self.code + \
                "(" + points + ": " + \
                self.name + '\n'


class CourseCollection():
    """ Data structure to store (unique) courses. """

    def __init__(self):
        self.courses = []
        self.headers = ["Course code", "Course name", "Main area(s)",
                "Level", "HP", "Period", "Block"]

    def is_empty(self):
        """ Returns True id CourseCollection contains no courses. """
        return not self.courses

    def add(self, new):
        """ Adds a course if it doesn't already exists among the courses.
        If it exists and span over several periods, updates the blocks.
        """
        for course in self.courses:
            if course == new and len(course.blocks) == 1:
                course.blocks = course.blocks + new.blocks 
                return
        self.courses.append(new)
        self.sort_on('name')
    
    def sort_on(self, factor, order = 'ascending'):
        """ Sorts courses on 'factor' in 'order', where
        factor = {'code',  'name', points',  'period', block'}
        order = {'rising', 'descending'}
        """
        key_fns = { 'code': (lambda c: c.code), 
                'name': (lambda c: c.name),
                'points': (lambda c: c.points),
                'period':(lambda c: c.period),
                'block': (lambda c: c.blocks)}

        self.courses.sort(key = key_fns[factor], reverse = order == 'descending')

    # TODO: Filter method?

    def to_csv(self):
        """ Returns a string: 
        a csv representation of the collection content. 
        """
        content = str(self.headers).strip("][").replace("'",'') + "\n" 
        for course in self.courses:
            row = "" \
                + course.code + ", " \
                + comma_to_csv(course.name) + ", " \
                + course.level + ", " \
                + comma_to_csv(course.areas) + ", " \
                + course.points + ", " \
                + course.period + ", " \
                + comma_to_csv(course.blocks) + "\n"
            content += row
        return content

    def to_html(self):
        """ Returns a string:
        an html representation of the collection content. 
        """
        html = "<!DOCTYPE html>\n" \
                + "<html>\n" \
                + head(script("text/javascript", "table_sorter.js") + 
                       title("Courses at U")) \
                + body(
                        heading("Courses at Mjukvaruteknik LiU") + 
                        paragraph(self.to_html_table())) \
                + "</html>"
        return html

    def to_html_table(self):
        """ Returns a string:
        the collection content as an html table.
        """
        res = "<table>\n"
        heads = ""
        for h in self.headers:
            heads += header(h)
        res += row(heads)

        for course in self.courses:
            data_row = "" \
                + data(course.code) \
                + data_left(hyperlink(course.name, course.url)) \
                + data_left(', '.join(course.areas)) \
                + data(course.level) \
                + data(course.points) \
                + data(course.period) \
                + data(', '.join(course.blocks))
            res += row(data_row)
        res += "</table>\n"
        return res

    def __iter__(self):
        return iter(self.courses)

    def __repr__(self):
        return ''.join(map(str, self.courses))
