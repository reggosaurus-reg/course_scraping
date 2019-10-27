# This file contains all the classes tied to representing courses.

class Course():
    """ Representation of a course. """

    def __init__(self, course, info, vtht, period_num):
        """ Takes a course tag 'course' and some info and extracts all 
        needed members.
        """
        # TODO: Go into url and fetch requirements, main subject etc.
        # TODO: Multithread the calls above
        self.code = course["data-course-code"] 
        self.name = course.a.text
        self.level = info[3]
        self.block = info[4]
        self.url = course.a["href"]

        # Handles courses spanning over several periods
        # period: VT/HT + 1, 2 or '*' (means both)
        points = info[2]
        if points[-1] == '*':
            self.points = points[:-1] 
            self.period = vtht + '*'  
        else:
            self.points = points
            self.period = vtht + period_num

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        """ Prints the course. """ 
        # TODO: Print info better - some sort of "compilable" excel? CSV?
        points = self.points
        points = points + ')' if len(points) == 2 else points + ') ' 
        return '[' + self.period + '] ' + \
                self.code + \
                "(" + points + ": " + \
                self.name + '\n'


# TODO: Does this really need to be a subclass?
class AdvancedCourse(Course):
    """ Representation of an advanced course. """

    def __init__(self, course, info, vtht, period_num):
        super().__init__(course, info, vtht, period_num)
        self.area = 'all main areas?'

    def __repr__(self):
        return str(super()) + ' (' + self.area + ')'


class CourseCollection():
    """ Data structure to store (unique) courses. """

    def __init__(self):
        # TODO: Make it a dict, with key being most frequent sorting field
        # Or several dicts, one for each key we'll sort after
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
        return 'COURSES: \n' + ''.join(map(str, self.courses))
