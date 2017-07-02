import React, { Component } from 'react';
import CoursesCollapsible from './CoursesCollapsible'
import CourseMeetingInfo from './CourseMeetingInfo'
import { getFullBuildingName, convertName } from '../helpers'


class CourseSectionList extends Component {
  // props: meetings, colors

  render() {
    let meetingList = this.props.meetings.map(
      meeting => {
        return (
          {
            key: meeting.name,
            leftHeaderIcon: (
              <i className="material-icons hide-on-small-only">filter_drama</i>
            ),
            leftHeaderText: (
              <span>
                Section {meeting.name}
              </span>
            ),
            rightHeaderText: (
              meeting.times[0].location
            ),
            bodyText: (
              <p>
                <span className="flow-text">
                  {meeting.instructors.map(instructor => {
                    return convertName(instructor)
                  }).join(", ")
                  }
                </span>
                <CourseMeetingInfo
                  meetings={this.props.meetings}
                  colors={this.props.colors}/>
              </p>
            )
          }
        )
      }
    )
    return (
      <CoursesCollapsible
        list={meetingList}
        extraClass="popout"
        colors={this.props.colors}/>
    )
  }
}

export default CourseSectionList;
