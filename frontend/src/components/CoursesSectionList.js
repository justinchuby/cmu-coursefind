import React, { Component } from 'react';
import Collapsible from './Collapsible'
import { daysToString, getFullBuildingName, convertName } from '../helpers'


class CourseList extends Component {
  // props: sections

  render() {
    let meetingList = this.props.sections.map(
      meeting => {
        let courseMeeingText = meeting.times.map(
          (time, index) => {
            return (
              <span key={index}>
                {time.days &&
                  <span>
                    <br/><i className="material-icons tiny">today</i>&nbsp;&nbsp;
                    {time.days.join(", ")}
                  </span>
                }
                {time.begin &&
                  <span>
                    <br/><i className="material-icons tiny">access_time</i>&nbsp;&nbsp;
                    From { time.begin } to { time.end }
                  </span>
                }
                {time.building &&
                  <span>
                    <br/><i className="material-icons tiny">explore</i>&nbsp;&nbsp;
                    {/* Add a google maps link to the building name if it is an
                        actual building */}
                    
                    {getFullBuildingName(time.building) ? (
                      <a href={`https://www.google.com/maps/search/${getFullBuildingName(time.building)}`}
                        target="_blank"
                        rel="nofollow noopener">
                        <b>{getFullBuildingName(time.building)}</b>
                      </a>
                    ) : (
                      <b>time.building</b>
                    )
                    }
                    {time.room}
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
                {currentCourseTime.building} {currentCourseTime.room} |
                {currentCourseTime.diffText}
              </span>
            ),
            rightHeaderTextShort: (
              <span>
                {currentCourseTime.building} {currentCourseTime.room} |
                {currentCourseTime.diffText}
              </span>
            ),
            bodyText: (
              <p className="grey-text text-lighten-5">
                <span className="flow-text">
                  <a className="amber-text text-accent-4" href={`/?q=${meeting.course.courseid}`}>
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
                <a className="waves-effect waves-light grey-text text-lighten-5"
                  href={`/courses/${meeting.course.courseid}/`}>
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
      <Collapsible list={meetingList} extraClassName="popout"/>
    )
  }
}

export default CourseList;
