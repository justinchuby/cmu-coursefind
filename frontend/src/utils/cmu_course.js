var moment = require('moment-timezone');


// moment.tz.add("America/New_York|EST EDT EWT EPT|50 40 40 40|01010101010101010101010101010101010101010101010102301010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010|-261t0 1nX0 11B0 1nX0 11B0 1qL0 1a10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 RB0 8x40 iv0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1a10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1cN0 1cL0 1cN0 1cL0 s10 1Vz0 LB0 1BX0 1cN0 1fz0 1a10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1a10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|21e6","America/New_York|EST EDT EWT EPT|50 40 40 40|01010101010101010101010101010101010101010101010102301010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010|-261t0 1nX0 11B0 1nX0 11B0 1qL0 1a10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 RB0 8x40 iv0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 WL0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1a10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1cN0 1cL0 1cN0 1cL0 s10 1Vz0 LB0 1BX0 1cN0 1fz0 1a10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 1cN0 1fz0 1a10 1fz0 1cN0 1cL0 1cN0 1cL0 1cN0 1cL0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|21e6")

export class Course {
  constructor(courseDict) {
    this.courseid = courseDict["id"]
    this.name = courseDict.name
    this.department = courseDict.department
    this.units = courseDict.units
    this.desc = courseDict.desc
    this.prereqs = courseDict.prereqs
    this.prereqs_obj = courseDict.prereqs_obj
    this.coreqs = courseDict.coreqs
    this.coreqs_obj = courseDict.coreqs_obj
    this.rundate = courseDict.rundate
    this.semester = courseDict.semester
    this.mini = 0
    const mini_match = this.semester.match(/(\d|[a-zA-Z])(\d)/)
    if (mini_match !== null) {
      this.mini = parseInt(mini_match[2])
    }

    this.lectures = courseDict.lectures.map(
      meeting => {
        return new Meeting(this, meeting)
      })
    this.sections = courseDict.sections.map(
      meeting => {
        return new Meeting(this, meeting)
      })
    this.instructors = []
    for (let lecture of this.lectures) {
      for (let instructor of lecture.instructors) {
        if (!(this.instructors.includes(instructor))) {
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
        return new TimeObj(time)
      })
    this.location = this.times[0].location
  }

  isHappeningOn(day) {
    // day is an integer in [0...6]
    for (const timeObj of this.times) {
      if (timeObj.isHappeningOn(day)) {
        return true
      }
    }
    return false
  }

  isHappeningAt(date_time) {
    for (const timeObj of this.times) {
      if (timeObj.isHappeningAt(date_time)) {
        return true
      }
    }
    return false
  }

  isHappeningNow() {
    return this.isHappeningAt(moment())
  }

  willHappenIn(minute) {
    for (const timeObj of this.times) {
      if (timeObj.willHappenIn(minute)) {
        return true
      }
    }
    return false
  }

  // nextTime() {
  //   next = null
  //   for (const timeObj of this.times) {
  //     if (next === null) {
  //       next = timeObj
  //     } else {
  //     }
  //   }
  // }

}

class TimeObj {
  constructor(timeDict) {
    this.days = timeDict["days"]
    this.location = timeDict["location"]
    this.building = timeDict["building"]
    this.room = timeDict['room']
    /* http://momentjs.com/docs/#/parsing/string-format/ */
    // TODO: check if moment works
    this.begin = moment.tz(timeDict["begin"], "HH:mmA", "America/New_York")
    this.end = moment.tz(timeDict["end"], "HH:mmA", "America/New_York")
    if (!this.begin.isValid()) {
      this.begin = null
    }
    if (!this.end.isValid()) {
      this.end = null
    }
  }

  isHappeningOn(day) {
    // day is an integer in [0...6]
    return (this.days.includes(day))
  }

  isHappeningAt(dateTime) {
    const day = dateTime.isoWeekday() % 7  // integer
    if (this.isHappeningOn(day) && (dateTime.isBetween(this.begin, this.end))) {
        return true
    }
    return false
  }

  isHappeningNow() {
    return this.isHappeningAt(moment())
  }

  willHappenInFrom(minute, dateTime) {
    dateTime.add(minute)
    return this.isHappeningAt(dateTime)
  }

  willHappenIn(minute) {
    // NOTE: KNOWN BUG: Does not deal with next-day events
    return this.willHappenInFrom(minute, moment())
  }
}
