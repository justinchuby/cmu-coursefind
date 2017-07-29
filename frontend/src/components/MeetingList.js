import React, { Component } from 'react';
// import { Link } from 'react-router-dom'
import Collapsible from './Collapsible'
import {
  daysToString,
  getFullBuildingName,
  convertName,
  getCurrentSemester } from '../helpers'


class MeetingList extends Component {
  constructor(props) {
    super(props);
    //   // TODO: how should I manipulate the course list?
  }

  render() {
    const meetingList = this.props.meetings.map(
      meeting => {
        const currentCourseTime = meeting.currentTimeObj() || meeting.nextTimeObj()
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
                    {time.begin.format("HH:mmA")}
                    <span className="grey-text text-lighten-2"> to </span>
                    {time.end.format("HH:mmA")}
                    <br /><br />
                  </span>
                }
              </span>
            )
          }
        )
        return (
          {
            key: meeting.course.courseid + meeting.name,
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
              (meeting.course.semester !== getCurrentSemester()) ? (
                <span>
                  {meeting.course.semester}
                </span>
              ) : (
                currentCourseTime ? (
                  <span>
                    {currentCourseTime.building} {currentCourseTime.room} | &nbsp;
                    {(currentCourseTime.isHappeningNow()) ? (
                        `Ends ${currentCourseTime.end.fromNow()}`
                      ) : (
                        `Begins ${currentCourseTime.begin.fromNow()}`
                      )
                    }
                  </span>
                ) : (
                  <span>
                    {daysToString(meeting.days)}
                  </span>
                )
              )
            ),
            rightHeaderTextShort: (
              // Same with rightHeaderText
              (meeting.course.semester !== getCurrentSemester()) ? (
                <span>
                  {meeting.course.semester}
                </span>
              ) : (
                currentCourseTime ? (
                  <span>
                    {currentCourseTime.building} {currentCourseTime.room} | &nbsp;
                    {(currentCourseTime.isHappeningNow()) ? (
                        `Ends ${currentCourseTime.end.fromNow()}`
                      ) : (
                        `Begins ${currentCourseTime.begin.fromNow()}`
                      )
                    }
                  </span>
                ) : (
                  <span>
                    {daysToString(meeting.days)}
                  </span>
                )
              )
            ),
            bodyText: (
              <p className="grey-text text-lighten-5">
                <span className="flow-text">
                  <a className="amber-text text-accent-4"
                    href={`/search?q=${meeting.course.courseid}`}
                    rel="nofollow">
                    {meeting.course.courseid}
                  </a> &nbsp;
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
