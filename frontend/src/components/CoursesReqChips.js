import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import Chip from './Chip'

class CoursesReqChips extends Component {
  render() {
    const splited = splitRequirementString(this.props.requirements)
    return (
      <span>
      {splited.map(
        (elem, index) => {
          if (elem.search(/\d{2}-\d{3}/) !== -1) {
            return (
              <Chip
                key={index}
                content={
                  <span>
                    <Link
                      to={`/courses/${elem}`}
                      className={this.props.colors.textMajorColor}>
                      {elem}
                    </Link>
                  </span>
                }
                style={{backgroundColor: "rgba(255, 255, 255, 0.2)"}} />
            )
          } else {
            return (
              <span key={index}>{elem}</span>
            )
          }
        }
      )}
      </span>
    )
  }
}

function splitRequirementString(requirements) {
  const re = /(\d{2}-\d{3})/
  const splited = requirements.split(re).map(elem => (elem.replace(/^\s+/,"")))
  return splited
}

export default CoursesReqChips;
