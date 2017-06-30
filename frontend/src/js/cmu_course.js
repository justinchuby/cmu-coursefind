class Course {
  constructor(courseDict) {
    this.courseid = courseDict["id"]
    this.lectures = courseDict.lectures.map(
      meeting => {
        return Meeting(this, meeting)
      })
    this.sections = courseDict.sections.map(
      meeting => {
        return Meeting(this, meeting)
      })
    this.instructors = []
    for (lec in this.lectures) {
      for (instructor in lec.instructors) {
        if (!(instructor in this.instructors)) {
          this.instructors.push(instructor)
        }
      }
    }
  }
}

class Meeting {
  constructor(course, meetingDict) {
    this.course = course
    this.name = meetingDict["name"]
    this.instructors = meetingDict["instructors"]
    this.times = meetingDict["times"].map(
      time => {
        return TimeObj(time)
      })
  }
}

class TimeObj {
  constructor(timeDict) {
    this.days = timeDict["days"]
    this.location = timeDict["location"]
    this.building = timeDict["building"]
    this.room = time['room']
    /* http://momentjs.com/docs/#/parsing/string-format/ */
    this.begin = moment.tz(timeDict["begin"], "HH:mmA", "America/New_York")
    this.end = moment.tz(timeDict["end"], "HH:mmA", "America/New_York")
  }
}
