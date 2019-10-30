import time
import requests
from bs4 import BeautifulSoup
from datastructures import *

# This file contains the runnable main structure  


def main():
    """ MAIN, ju. """
    ## Get data
    page = requests.get('https://liu.se/studieinfo/program/6cmju/4208#')
    soup = BeautifulSoup(page.text, features="html5lib") 
    # TODO: Read from file with finished courses... 

    ## Process data
    # TODO: ...then filter those courses from found courses
    found_courses = find_courses(soup) # Add false to include not advanced
    found_courses.sort_on('period')

    ## Present data
    #print(found_courses)
    generate_html(found_courses, "courses.html")
    

def generate_html(data, filename):
    """ Creates (or overwrites) an html representation of CourseCollection 
    'data' in the file 'filename'.
    """
    ## Functions for encapsulating content in correct html syntax
    head = lambda content: "\n<head>\n" + content + "</head>\n"
    body = lambda content: "\n<body>\n" + content + "</body>\n"
    title = lambda content: "<title>" + content + "</title>\n"
    heading = lambda content: "<h1>" + content + "</h1>\n"
    paragraph = lambda content: "<p>" + content + "</p>\n"

    # TODO: Warn if file exists and prompt the user to be sure to overwrite
    ## To empty the file
    with open(filename, 'w') as f:
        f.write("<!DOCTYPE html>")

    # TODO: Generate one string and write only that?
    # i.e. call to_html() in every data object

    ## Write html content
    with open(filename, 'a') as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write(head(title("Test course heading")))
        f.write(body(
            # TODO: Write the courses in an ordered manner!
            # - newlines
            # - subheadings for ht/vt
            heading("COURSES") + 
            paragraph(str(data))))
        f.write("</html>")

    # TODO: Make html interactive - online necessary?


def find_courses(soup, only_advanced=True):
    """ Prints all course codes. 
    (Only advanced course codes if that option is not turned off.)
    """
    found_courses = CourseCollection() 

    for semester_tag in soup.find_all('article', 
            attrs={'class': 'accordion box semester js-semester is-toggled'}):
        when = str(semester_tag.header.h3).split('(')[1][:-6]
        vtht, year = when.split()
            
        for period_tag in semester_tag.find_all('tbody', attrs={'class': 'period'}):
            vthtnum = str(period_tag.th.text).split()[1]

            for course_tag in period_tag.find_all('tr', attrs={'class': 'main-row'}):
                ## Filter courses
                info = extract_tds(course_tag)
                if only_advanced:
                    level = info[3]
                    if level[0] != "A":
                        continue

                found_courses.add(Course(course_tag, info, vtht, vthtnum))

    return found_courses


def extract_tds(course):
    """ Takes a tag 'course' and gives a list with all of its td tags. """
    res = []
    for td in course.find_all('td'):
        res.append(str(td).strip()[4:-5])
    return res


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Execution took", time.time() - start_time, "seconds.")
