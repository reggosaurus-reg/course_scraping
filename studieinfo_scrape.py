import requests
from bs4 import BeautifulSoup


def main():
    """ MAIN, ju. """
    page = requests.get('https://liu.se/studieinfo/program/6cmju/4208#')
    soup = BeautifulSoup(page.text, features="html5lib") 
    find_advanced(soup)
    

def extract_tds(course):
    """ Takes a tag 'course' and gives a list with all of its td tags. """
    res = []
    for td in course.find_all('td'):
        res.append(str(td).strip()[4:-5])
    return res


def find_advanced(soup):
    """ Prints all advanced course codes. """
    for course in soup.find_all('tr', attrs={'class': 'main-row'}):
        info = extract_tds(course)
        level = info[3]
        # Filter courses
        if level[0] != "A":
            continue

        # Retrieve all course info
        # TODO: Go into url and fetch HT/VT, requirements, main subject etc.
        course_code = course["data-course-code"]
        course_name =  course.a.text
        points = info[2]
        over_two_periods = points[-1] == '*'
        if over_two_periods:
            points = points[:-1] 
        url = course.a["href"]
        block = info[4]

        print(AdvancedCourse(course_code, course_name, points, over_two_periods + 1, block, url))


def sort_courses(courses, factor, order):
    """ Returns a version of list 'courses', sorted on 'factor' 
    in 'order', where
    factor = {'code', 'points', 'block'}
    order = {'rising', 'descending'}
    """
    # TODO: Implement
    return courses


class AdvancedCourse():
    """ Representation of an advanced course. """

    # TODO: Initialize here - only take course tag
    def __init__(self, code, name, points, periods, block, url):
        self.code = code 
        self.name = name
        self.points = points
        self.periods = periods
        self.block = block
        self.url = url

    # TODO: Print info better - some sort of "compilable" excel?
    def __repr__(self):
        return self.code + "(" + self.points + ")" + ": " + self.name 

if __name__ == "__main__":
    main()
