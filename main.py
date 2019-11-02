import time
import threading
import requests
from bs4 import BeautifulSoup
from datastructures import *

# This file contains the runnable main structure  


def main():
    """ MAIN, ju. """
    ## Get data
    print("Downloading... (0%)\r", end='')
    page = requests.get('https://liu.se/studieinfo/program/6cmju/4208#')
    soup = BeautifulSoup(page.text, features="html5lib") 
    # TODO: Read from file with finished course codes (or ladok)...
    # ...then mark those courses with a tag and make a css class
    # TODO: Only fetch data if haven't fetch for... a week? Save it somewhere.
    # ... perhaps a csv, this time?

    ## Process data

    found_courses = find_courses(soup) # Add false to include not advanced

    # TODO: Some database like sorting on (several) field with JavaScript...
    found_courses.sort_on('block')

    ## Present data
    write(found_courses.to_html(), "courses.html", "html", unsafe=True)
    #write(found_courses.to_csv(), "courses_csv.txt", "csv")


def find_courses(soup, only_advanced=True):
    """ Prints all course codes. 
    (Only advanced course codes if that option is not turned off.)
    """
    found_courses = CourseCollection() 

    threads = []
    stop_threads = False
    for semester_tag in soup.find_all('article', 
            attrs={'class': 'accordion box semester js-semester is-toggled'}):
        when = str(semester_tag.header.h3).split('(')[1][:-6]
        vtht, year = when.split()
            
        for period_tag in semester_tag.find_all('tbody', attrs={'class': 'period'}):
            vthtnum = str(period_tag.th.text).split()[1]

            ## For threading
            def find_courses_in_period():
                """ Finds and the courses in period_tag. """
                for course_tag in period_tag.find_all('tr', attrs={'class': 'main-row'}):
                    ## Filter courses
                    info = extract_tds(course_tag)
                    if only_advanced:
                        level = info[3]
                        if level[0] != "A":
                            continue

                    found_courses.add(Course(course_tag, info, vtht, vthtnum))
                    if not found_courses.is_empty():
                        return
                    nonlocal stop_threads
                    if stop_threads:
                        break

            thread = threading.Thread(target=find_courses_in_period)
            threads.append(thread)
            thread.start()


    ## Show progress
    finished = 0
    total = len(threads)
    while threads:
        try:
            for thread in threads:
                if not thread.is_alive():
                    thread.join()
                    threads.remove(thread)
                    finished += 1
                    print("Downloading... (" + \
                            str(round(100 * finished/total)) + "%)\r" , end='')
        ## Abort download
        except KeyboardInterrupt:
            print("Downloading... (" + \
                    str(round(100 * finished/total)) + "%) \nAborting...")
            stop_threads = True
            time.sleep(1)
            for thread in threads:
                thread.join()
            exit("Yay, download was aborted!")

    return found_courses


def extract_tds(course):
    """ takes a tag 'course' and gives a list with all of its td tags. """
    res = []
    for td in course.find_all('td'):
        res.append(str(td).strip()[4:-5])
    return res


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Execution took", round(time.time() - start_time, ndigits=2), "seconds.")
