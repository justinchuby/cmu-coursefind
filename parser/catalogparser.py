# readFile() and writeFile() come from CMU 15112 class notes

from html.parser import HTMLParser
import coursecat, cmu_prof
import copy
import json


def main():
    print("""To parse a catalog to test, use write_SOC_to_text()
             to parse to JSON, use write_SOC_to_JSON()""")

main()


SOC_TABLE_ORDER = {
    "number": 0,
    "name": 1,
    "units": 2,
    "lecsec": 3,
    "days": 4,
    "beginTime": 5,
    "endTime": 6,
    "room": 7,
    "location": 8,
    "instructor": 9
}


class CatalogParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # self.currentTag = None
        self.currentTags = set()  # self.currentTags is a set
        self.course = []
        self.result = []
        self.temp = dict()

    def reset(self):
        HTMLParser.reset(self)
        self.result = []

    def handle_starttag(self, tag, attrs):
        self.currentTags.add(tag)

    def handle_endtag(self, tag):
        _ORDER = SOC_TABLE_ORDER
        if tag == "tr":
            # runs to the end of a line, create a Course istance and put it into the list

            # deal with one-course-in-two-line type
            # store in temp first, then place the info into the next list

            # deal with course with recitations at different places on different days
            if len(self.course) == 9 and self.course[_ORDER["days"]].isalpha():
                self.course.append(" ")
            try:
                if self.course[_ORDER["name"]].endswith(":"):
                    self.temp["number"] = self.course[_ORDER["number"]]
                    self.temp["name"] = self.course[_ORDER["name"]]
                    self.temp["units"] = self.course[_ORDER["units"]]
                else:
                    # if self.course[_ORDER["number"]].isalpha():
                    #     print(self.course, "!!alpha")
                    if not self.course[_ORDER["number"]].isdigit() and not self.course[_ORDER["number"]].isalpha():
                        self.course[_ORDER["number"]] = self.temp.get("number", " ")
                        if self.course[_ORDER["name"]] == "":
                            self.course[_ORDER["name"]] = self.temp.get("name", " ")
                        self.course[_ORDER["units"]] = self.temp.get("units", " ")
                    self.result.append(self.course)
                    self.temp = dict()
            except IndexError:
                print("IndexError")
                self.result.append(self.course)

            # print(self.course, "++")
            # store the course list into result
            self.course = []

        # disgard the tag anyway
        self.currentTags.discard(tag)

    def handle_data(self, data):
        if self.inTag("td"):  # this may not work with <td><td>data</td></td>
            # deal with the "&" sign
            data = data.replace("[amp]", "&")
            data = data.strip()
            if data == "":
                data = " "
            self.course.append(data)

    def inTag(self, tag):
        return tag in self.currentTags

    def output(self):
        return self.result


def openFile(path):
    with open(path, "rt") as f:
        return f.read()


def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def getProf(courseList):
    EMPTY = coursecat.Empty()
    newCourses = []
    for course in courseList:
        if course.instructor != EMPTY:
            instructors = coursecat.splitString(course.instructor.lower())
            for i in range(len(instructors)):
                instructors[i] = cmu_prof.getFullName(course, instructors[i])
            newInstructor = ", ".join(instructors)
            course.updateKey("instructor", newInstructor)
            newCourses.append(course)
    return newCourses


def parseSOC(path):
    def completeCourses(courseList):
        # takes in a list of courses and returns a completed list of courses
        EMPTY = coursecat.Event.EMPTY
        newCourses = []
        prevCourse = coursecat.SOCCourse()
        for course in courseList:
            print("--", prevCourse)
            print(">>", course)
            print(course.isCompleted())
            if not course.isCompleted():
                for key, value in course.content().items():
                    if value == EMPTY:
                        value = prevCourse.get(key, coursecat.Event.EMPTY)
                        course.updateKey(key, value)
                print("<<", course)

            newCourses.append(course)
            prevCourse = course
        return newCourses



    parser = CatalogParser()
    f = openFile(path)

    parsedCatalog = []
    courses = []

    f = f.replace("&nbsp;", " ")
    f = f.replace("&", "[amp]")
# DEBUG
    # print("& index", f.find("&"))

    parser.feed(data=f)
    parsedCatalog = parser.output()
    for elem in parsedCatalog:
        course = coursecat.SOCCourse(elem)
        if course.isLegal() and (not course.isEmpty()):
            courses.append(course)
    courses = completeCourses(courses)
    courses = getProf(courses)
    return courses


def parseCSV(path):
    f = openFile(path)
    courses = []
    parsedCatalog = f.split("\n")
    order = copy.copy(coursecat.Event.KEYS)

    for line in parsedCatalog:
        L = line.split(",")
        course = coursecat.Course()
        for i in range(len(order)):
            if i < len(L):
                course.updateKey(order[i], L[i])
        if course.isLegal() and (not course.isEmpty()):
            courses.append(course)
    return courses


def outputJSON(courses, arg=None):
    outputCourses = [course.JSONDict() for course in courses]
    if arg == "Parse":
        outputCourses = {"results": outputCourses}
    result = json.dumps(outputCourses, sort_keys=True, indent=4)
    return result


def writeFileToPath(s, path=None):
    outputPath = ""
    # while outputPath != "exit":
    #     try:
    if path is None:
        outputPath = input("output path:")
    else:
        outputPath = path
    print("writing...")
    writeFile(outputPath, s)
    print("Succeeded!")
    return
        # except:
        #     print("Write failed...")


def parseSOCFromPath():
    path = input('SOC path: ')
    print("parsing...")
    courses = parseSOC(path)
    print("parsed")
    return courses


def write_SOC_to_JSON():
    courses = parseSOCFromPath()
    JSONToWrite = outputJSON(courses, "Parse")
    writeFileToPath(JSONToWrite)


def write_SOC_to_text():
    courses = parseSOCFromPath()
    outputCatalog = ""
    for course in courses:
        outputCatalog += str(course) + "\n"
    writeFileToPath(outputCatalog)


def print_SOC():
    courses = parseSOCFromPath()
    outputCatalog = ""
    for course in courses:
        outputCatalog += str(course) + "\n"
    print(outputCatalog)


#################################
def test_parse():
    print("parsing...")
    # courses = parseSOC("Course_Catalog/SOC_S16.html")
    courses = parseSOC("Course_Catalog/Carnegie Mellon University - Full Schedule Of Classes.html")
    # courses = parseSOC("Course_Catalog/sched_layout_spring.html")
    print("parsed")

    print("writing")

    outputCatalog = ""
    for course in courses:
        outputCatalog += str(course) + "\n"
    writeFile("test.txt", outputCatalog)

    print("succeeded!")


def test_parseStored():
    courses = parseCSV("test.txt")
    print("parsed")
    print(courses)


def testAll():
    # test_parse()
    return 42

if __name__ == "__main__":
    testAll()
