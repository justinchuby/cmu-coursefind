import React, { Component } from 'react';
import CoursesCollapsible from './CoursesCollapsible'
import { getFullBuildingName, convertName } from '../helpers'


class CourseMeetingInfo extends Component {
  // props: meetings

  render() {
    let meetingInfo = meeting.times.map(
      (time, index) => {
        return (
          <span key={index}>
            <br />
            {time.days &&
              <span>
                <br /><i className="material-icons tiny">today</i>&nbsp;&nbsp;
                    {time.days.join(", ")}
              </span>
            }
            {time.begin &&
              <span>
                <br /><i className="material-icons tiny">access_time</i>&nbsp;&nbsp;
                From {time.begin} to {time.end}
              </span>
            }
            {time.building &&
              <span>
                <br /><i className="material-icons tiny">explore</i>&nbsp;&nbsp;
                {/* Add a google maps link to the building name if it is an
                    actual building */}

                {getFullBuildingName(time.building) ? (
                  <a href={`https://www.google.com/maps/search/${getFullBuildingName(time.building)}`}
                    className={this.props.colors.textAccentColor}
                    target="_blank"
                    rel="nofollow noopener">
                    <b>{getFullBuildingName(time.building)}</b>
                  </a>
                ) : (
                    <b>{time.building}</b>
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
      { meetingInfo }
    )
  }
}

export default CourseMeetingInfo;
