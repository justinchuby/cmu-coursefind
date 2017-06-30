import React, { Component } from 'react';
import CollapsibleElement from './CollapsibleElement'
import { daysToString, getFullBuildingName } from './helpers'


function titleCase(str) {
  return str.toLowerCase().replace(/\b(\w)/g, s => s.toUpperCase());
}

class CourseList extends Component {
  constructor(props) {
    super(props);
    // this.state = {
    //   courses = props.
    // }
  }

  render() {
    let courseList = this.props.courses.map(
      course => {
        let currentCourseTime = course.current
        let courseMeeingText = course.times.map(
          time => {
            return (
              <span>
                {daysToString(time.days)} &nbsp; | {getFullBuildingName(time.building) &&
                  `<a className="amber-text text-accent-4" href="https://www.google.com/maps/search/${getFullBuildingName(time.building)}" target="_blank">
                 ${getFullBuildingName(time.building)}</a> ${time.room}`}
                <br/>
                {time.begin &&
                  `<span className="grey-text text-lighten-2">From</span>
                  ${time.begin}
                  <span className="grey-text text-lighten-2">to</span>
                  ${time.end}
                  <br/><br/>`
                }
              </span>
            )
          }
        )
        return (
          {
            leftHeaderText:
              <span>
                {course.courseid} &nbsp;
                {course.lecsec != "Lec" &&
                  course.lecsec
                }
                &nbsp;&nbsp;
                {course.name}
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
                  <a className="amber-text text-accent-4" href={`/?q=${course.courseid}`}>
                    {course.courseid}
                  </a> &nbsp; 
                  {course.name} &nbsp; 
                  {course.lecsec} &nbsp;
                </span>
                <br/><br/>
                / &nbsp; {course.department} &nbsp; / <br/>
                {courseMeeingText}
                {/* TODO */}
                <span className="grey-text text-lighten-2">Instructor:</span> &nbsp;
                {titleCase(course.instructors.join(", "))}
                <br/><br/>
                <a className="waves-effect waves-light grey-text text-lighten-5"
                  href={`/courses/${course.courseid}/`}>
                  {"<"}
                  {/* TODO: make this more like a button */}
                  More
                    <span className="amber-text text-accent-4">details</span>
                  about this course 
                  {">"}
                </a>
              </p>
          }
        )
      }
    )
    return (
      <Collapsible list={list}/>
    )
  }
}

export default CourseList;
