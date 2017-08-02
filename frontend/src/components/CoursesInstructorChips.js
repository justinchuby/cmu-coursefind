import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import Chip from './Chip'
import { convertName } from '../helpers'

class CoursesInstructorChips extends Component {

  render() {
    return (
      <div>
      {this.props.instructors.map(
        instructor => {
          const name = convertName(instructor)
          return (
            <Chip
              key={instructor}
              content={
                <span>
                  <Link to={`/search/?q=${name}`} className="grey-text text-darken-3">
                    {name}
                  </Link>
                  {/* &nbsp;&nbsp;
                  <a className="waves-effect grey-text text-darken-3"
                    href={`http://www.ratemyprofessors.com/search.jsp?query=${instructor}`}
                    target="_blank" rel="nofollow">
                    <i className="material-icons tiny">launch</i>
                  </a> */}
                </span>
              }
              extraClass="hoverable" />
          )
        }
      )}
      </div>
    )
  }
}

export default CoursesInstructorChips;
