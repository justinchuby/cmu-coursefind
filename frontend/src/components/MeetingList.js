import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import Collapsible from './Collapsible'
import {
  daysToString,
  getFullBuildingName,
  convertName,
  getCurrentSemester,
  getMini
} from '../helpers'


class MeetingList extends Component {
  constructor(props) {
    super(props);
    //   // TODO: how should I manipulate the course list?
  }

  getRightHeaderText(meeting) {
    //meeting.course.mini !== 0 && meeting.course.mini !== getMini()
    if (meeting.course.semester !== getCurrentSemester()) {
      // Not the current semester, show semester
      return (
        <span>
          {meeting.course.semester}
        </span>
      )
    } else if (meeting.course.mini !== 0 && meeting.course.mini !== getMini()) {
      // Not the corrent Mini
      return (
        <span>
          Mini {meeting.course.mini}
        </span>
      )
    } else {
      const currentCourseTime = meeting.currentTimeObj() || meeting.nextTimeObj()
      if (currentCourseTime) {
        // Show at what time it will begin/end
        return (
          <span>
            {currentCourseTime.building} {currentCourseTime.room} | &nbsp;
            {(currentCourseTime.isHappeningNow()) ? (
              `Ends ${currentCourseTime.end.fromNow()}`
            ) : (
                `Begins ${currentCourseTime.begin.fromNow()}`
              )
            }
          </span>
        )
      } else {
        return (
          <span>
            {daysToString(meeting.days)}
          </span>
        )
      }
    }
  }

  render() {
    const meetingList = this.props.meetings.map(
      meeting => {
        const courseMeeingText = meeting.times.map(
          (time, index) => {
            return (
              <span key={index}>
                {time.days && `${daysToString(time.days)}`}
                {
                  time.building ? (
                    getFullBuildingName(time.building) ? (
                      /* if the building abbreviation is known,
                         display the full name
                      */
                      <span>
                        &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                        <a className="amber-text text-accent-4"
                          href={`https://www.google.com/maps/search/${getFullBuildingName(time.building)}`}
                          target="_blank" rel="nofollow">
                          {getFullBuildingName(time.building)}
                        </a>
                        &nbsp;
                        {time.room}
                      </span>
                    ) : (
                        /* if the building abbreviation is not known, display
                           the abbr
                        */
                        <span>
                          &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                        {time.building} {time.room}
                        </span>
                      )
                  ) : (
                      /* if the building is null */
                      null
                    )
                }
                <br />
                {time.begin &&
                  <span>
                    <span className="grey-text text-lighten-2"> From </span>
                    {time.begin.format("h:mm a")}
                    <span className="grey-text text-lighten-2"> to </span>
                    {time.end.format("h:mm a")}
                    <br /><br />
                  </span>
                }
              </span>
            )
          }
        )
        return (
          {
            key: meeting.course.courseid + meeting.name + meeting.course.semester,
            leftHeaderIcon: (
              <i className="material-icons hide-on-small-only">class</i>
            ),
            leftHeaderText: (
              <span>
                {meeting.course.courseid} &nbsp;
              {meeting.name !== "Lec" &&
                  meeting.name
                }
                &nbsp;&nbsp;
                {meeting.course.name}
              </span>
            ),
            rightHeaderText: (
              this.getRightHeaderText(meeting)
            ),
            rightHeaderTextShort: (
              // Same with rightHeaderText
              this.getRightHeaderText(meeting)
            ),
            bodyText: (
              <p className="grey-text text-lighten-5">
                <span className="flow-text">
                  <Link className="amber-text text-accent-4"
                    to={`/search?q=${meeting.course.courseid}`}
                    rel="nofollow">
                    {meeting.course.courseid}
                  </Link> &nbsp;
                  {meeting.course.name} &nbsp;
                  {meeting.name} &nbsp;
                </span>
                <br /><br />
                / &nbsp; {(meeting.course.department)} &nbsp; /
                <br />
                {courseMeeingText}
                <span className="grey-text text-lighten-2">Instructor:</span> &nbsp;
                {meeting.instructors.map(instructor => {
                  return convertName(instructor)
                }).join(", ")
                }
                <br /><br />
                <a
                  href={`/courses/${meeting.course.courseid}/`}
                  className="waves-effect waves-light grey-text text-lighten-5">
                  {"< "}
                  {/* TODO: make this more like a button */}
                  More
                  <span className="amber-text text-accent-4"> details </span>
                  about this course
                  {" >"}
                </a>
              </p>
            )
          }
        )
      }
    )
    return (
      <Collapsible list={meetingList} />
    )
  }
}

export default MeetingList;
