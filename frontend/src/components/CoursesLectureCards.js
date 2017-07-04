import React, { Component } from 'react';
import Card from './Card'
import CoursesMeetingInfo from './CoursesMeetingInfo'
import { convertName } from '../helpers'

class CoursesLectureCards extends Component {
  // props: meetings, colors

  cardContent(meeting) {
    return (
      <span>
        <p className="right-align">
          <span className="light">{meeting.times[0].location}</span>
        </p>
        <p className="right-align">
          {meeting.instructors.map(
            instructor => {
              return (
                <a 
                  key={instructor}
                  className={this.props.colors.textMajorColor}>
                  <b>{convertName(instructor)}</b><br />
                </a>
              )
            }
          )}
        </p>
        <p>
          <CoursesMeetingInfo
            times={meeting.times}
            colors={this.props.colors}/>
        </p>
      </span>
    )
  }

  render() {
    return (
      <div className="row">
        {this.props.meetings.map(
          meeting => {
            return (
              <div key={meeting.name} className="col s12 m6 l4">
                <Card
                  cardColor={this.props.colors.majorColor}
                  extraClass="hoverable"
                  textColor={this.props.colors.textMajorColor}
                  title={<b>&nbsp;&nbsp;&nbsp;{meeting.name}</b>}
                  content={this.cardContent(meeting)}
                />
              </div>
            )
          }
        )}
      </div>
    );
  }
}

export default CoursesLectureCards;
