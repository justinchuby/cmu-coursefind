import React, {Component } from 'react';
import CollapsibleElement from './CollapsibleElement'

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
              // TODO: fix here
              <span>
                {time.days_text} &nbsp; | {% if time.building_text %}<a className="amber-text text-accent-4" href="https://www.google.com/maps/search/{time.building_text}" target="_blank">
                 {time.building_text} </a> {time.room}{% endif %}<br/>
                {% if time.begin %}<span className="grey-text text-lighten-2">From</span> {time.begin} <span className="grey-text text-lighten-2">to</span> {time.end} <br/><br/>{% endif %}
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
                  <a className="amber-text text-accent-4" href={"/?q=" + course.courseid}>
                    {course.courseid}
                  </a> &nbsp; 
                  {course.name} &nbsp; 
                  {course.lecsec} &nbsp;
                </span>
                <br/><br/>
                / &nbsp; {course.department} &nbsp; / <br/>
                {courseMeeingText}

                <span className="grey-text text-lighten-2">Instructor:</span> &nbsp;
                {course.instructors|join:", "|title}
                <br/><br/>
                <a className="waves-effect waves-light grey-text text-lighten-5"
                  href={"/courses/" + course.courseid + "/"}>
                  {"<"} More
                  <span className="amber-text text-accent-4">details</span>
                  about this course {">"}
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
