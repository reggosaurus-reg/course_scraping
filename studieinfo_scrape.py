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
    foundCourses = CourseCollection() 

    for semester_tag in soup.find_all('article', attrs={'class': 'accordion box semester js-semester is-toggled'}):
        when = str(semester_tag.header.h3).split('(')[1][:-6]
        vtht, year = when.split()
            
        for period_tag in semester_tag.find_all('tbody', attrs={'class': 'period'}):
            vthtnum = str(period_tag.th.text).split()[1]
            for course in period_tag.find_all('tr', attrs={'class': 'main-row'}):
                info = extract_tds(course)
                level = info[3]
                ## Filter courses
                #if level[0] != "A":
                #    continue

                # TODO: Go into url and fetch requirements, main subject etc.
                ## Retrieve all course info
                course_code = course["data-course-code"]
                course_name =  course.a.text
                url = course.a["href"]
                block = info[4]
                points = info[2]
                # Courses spanning over several periods
                if points[-1] == '*':
                    points = points[:-1] 
                    period = vtht + '*'
                else:
                    period = vtht + vthtnum

                ## Save course info
                foundCourses.add(Course(course_code, course_name, points, 
                                        level, period, block, url))
    
    foundCourses.sort_on('period')
    print(foundCourses)
    with open('courses.txt', 'w') as f:
        f.write(str(foundCourses))


##### Classes #####


class Course():
    """ Representation of a course. """

    # TODO: Initialize here - only take course tag
    def __init__(self, code, name, points, level, period, block, url):
        self.code = code 
        self.name = name
        self.points = points
        self.level = level
        self.period = period # VT/HT + 1, 2 or '*' (means both)
        self.block = block
        self.url = url

    def __eq__(self, other):
        return self.code == other.code

    # TODO: Print info better - some sort of "compilable" excel?
    def __repr__(self):
        points = self.points
        points = points + ')' if len(points) == 2 else points + ') ' 
        return '[' + self.period + '] ' + \
                self.code + \
                "(" + points + ": " + \
                self.name 


# TODO: Does this really need to be a subclass?
class AdvancedCourse(Course):
    """ Representation of an advanced course. """

    def __init__(self, code, name, points, period, block, url):
        super().__init__(code, name, points, 'A', period, block, url)
        self.area = 'all main areas?'

    def __repr__(self):
        return str(super()) + ' (' + self.area + ')'


class CourseCollection():
    """ Data structure to store (unique) courses. """

    def __init__(self):
        self.courses = []

    def add(self, new):
        """ Adds a course if it doesn't already exists among the courses. """
        for course in self.courses:
            if course == new:
                return
        self.courses.append(new)

    def sort_on(self, factor, order = 'ascending'):
        """ Sorts courses on 'factor' in 'order', where
        factor = {'code', 'points',  'period', block'}
        order = {'rising', 'descending'}
        """
        key_fns = { 'code': (lambda c: c.code), 
                'points': (lambda c: c.points),
                'period':(lambda c: c.period),
                'block': (lambda c: c.block)}

        self.courses.sort(key = key_fns[factor], reverse = order == 'descending')

    def __repr__(self):
        return 'COURSES: ' + \
                ''.join(['\n' + str(course) for course in self.courses])


if __name__ == "__main__":
    main()
