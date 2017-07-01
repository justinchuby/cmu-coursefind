import React, { Component } from 'react';
import Collapsible from './Collapsible'
import { daysToString, getFullBuildingName, convertName } from '../helpers'


class CourseList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: props.courses,
      // get the lectures out from each course and reduce them from 2D
      // array to 1D array
      lectures: props.courses.map(
        course => {
          return course.lectures
        }).reduce(
        (a, b) => a.concat(b), []
        ),
      sections: props.courses.map(
        course => {
          return course.sections
        }).reduce(
        (a, b) => a.concat(b), []
        )
      // TODO: how should I manipulate the course list?
    }
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      courses: nextProps.courses,
      // get the lectures out from each course and reduce them from 2D
      // array to 1D array
      lectures: nextProps.courses.map(
        course => {
          return course.lectures
        }).reduce(
        (a, b) => a.concat(b), []
        ),
      sections: nextProps.courses.map(
        course => {
          return course.sections
        }).reduce(
        (a, b) => a.concat(b), []
        )
    })
  }

  render() {
    // TODO: fix this
    let meetingList = this.state.lectures.map(
      meeting => {
        // TODO: fix this
        let currentCourseTime = meeting.times[0]
        let courseMeeingText = meeting.times.map(
          (time, index) => {
            return (
              <span key={index}>
                {daysToString(time.days)} &nbsp; |
                &nbsp;
                {getFullBuildingName(time.building) &&
                  <span>
                    <a className="amber-text text-accent-4"
                      href={`https://www.google.com/maps/search/${getFullBuildingName(time.building)}`}
                      target="_blank">
                      {getFullBuildingName(time.building)}
                    </a>
                    &nbsp;
                    {time.room}
                  </span>
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
            leftHeaderText:
            <span>
              {meeting.course.courseid} &nbsp;
                {meeting.name !== "Lec" &&
                meeting.name
              }
              &nbsp;&nbsp;
                {meeting.course.name}
            </span>,
            rightHeaderText:
            <span>
              {currentCourseTime.building} {currentCourseTime.room} |
                {currentCourseTime.diffText}
            </span>,
            rightHeaderTextShort:
            <span>
              {currentCourseTime.building} {currentCourseTime.room} |
                {currentCourseTime.diffText}
            </span>,
            bodyText:
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
          }
        )
      }
    )
    return (
      <Collapsible list={meetingList} />
    )
  }
}

export default CourseList;
