import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import Collapsible from './Collapsible'
import { daysToString, getFullBuildingName, convertName } from '../helpers'


class MeetingList extends Component {
  constructor(props) {
    super(props);
    //   // TODO: how should I manipulate the course list?
  }

  render() {
    // TODO: fix this
    const meetingList = this.props.meetings.map(
      meeting => {
        // TODO: fix this
        const currentCourseTime = meeting.times[0]
        const courseMeeingText = meeting.times.map(
          (time, index) => {
            return (
              <span key={index}>
                {time.days && `${daysToString(time.days)}  | `}
                {/* TODO: check the DNM case */}
                {getFullBuildingName(time.building) ? (
                  <span>
                    <a className="amber-text text-accent-4"
                      href={`https://www.google.com/maps/search/${getFullBuildingName(time.building)}`}
                      target="_blank" rel="nofollow">
                      {getFullBuildingName(time.building)}
                    </a>
                    &nbsp;
                    {time.room}
                  </span>
                  ) : (
                    <span>
                      {time.building} {time.room}
                    </span>
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
              <span>
                {currentCourseTime.building} {currentCourseTime.room} | &nbsp;
                {/* TODO: Fix here */}
                {currentCourseTime.begin && currentCourseTime.begin.fromNow()}
              </span>
            ),
            rightHeaderTextShort: (
              <span>
                {currentCourseTime.building} {currentCourseTime.room} | &nbsp;
                {/* TODO: Fix here */}
                {currentCourseTime.begin && currentCourseTime.begin.fromNow()}
              </span>
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
                  console.log(instructor)
                  return convertName(instructor)
                }).join(", ")
                }
                <br /><br />
                <Link 
                  to={`/courses/${meeting.course.courseid}/`}
                  className="waves-effect waves-light grey-text text-lighten-5">
                  {"< "}
                  {/* TODO: make this more like a button */}
                  More
                  <span className="amber-text text-accent-4"> details </span>
                  about this course
                  {" >"}
                </Link>
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
