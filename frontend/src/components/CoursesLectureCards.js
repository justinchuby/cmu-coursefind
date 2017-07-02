import React, { Component } from 'react';
import Card from './Card'
import CourseMeetingInfo from './CourseMeetingInfo'
import convertNames from '../helpers'

class CoursesLectureCards extends Component {
  // props: meetings, cardColor, textColor, textAccentColor

  cardContent() {
    return (
      <span>
        <p class="right-align">
          <span class="light">{meeting.times[0].location}</span>
        </p>
        <p class="right-align">
          {meeting.instructors.map(
            instructor => {
              return (
                <a class={this.props.colors.textColor}><b>{convertName(instructor)}</b><br /></a>
              )
            }
          )}
        </p>
        <p>
          <CourseMeetingInfo
            meetings={this.props.meetings}
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
              <div className="col s12 m6 l4">
                <Card
                  cardColor={this.props.colors.cardColor}
                  extraClass="hoverable"
                  textColor={this.props.colors.textColor}
                  title={<b>&nbsp;&nbsp;&nbsp;{meeting.name}</b>}
                  content={cardContent()}
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
