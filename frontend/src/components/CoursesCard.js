import React, { Component } from 'react';
import Card from './Card'
import Dropdown from './Dropdown'
import Chip from './Chip'
import CoursesReqChips from './CoursesReqChips'
import {
  compareSemesters,
  semesterToAbbr
} from '../helpers'
import { Link } from 'react-router-dom'

class CoursesCard extends Component {
  // props: semester, courses, colors:{majorColor, textMajorColor, courseidColor, textAccentColor}
  cardContent() {
    const course = this.props.courses[this.props.semester]
    return (
      <div>
        <div className="row">
          <div className="col m9 offset-m1 offset-l2">
            <h1 className={`light ${this.props.colors.courseidColor}`}>
              {course.courseid}
              <Chip
                content={
                  <span className={`flow-text ${this.props.colors.textMajorColor}`}>
                    <Dropdown
                      name="semester-dropdown"
                      content={course.semester}
                      dropdownContents={
                        Object.values(this.props.courses)
                          .sort((a, b) => compareSemesters(a.semester, b.semester))
                          .reverse()
                          .map(value => 
                            <Link to={`/courses/${course.courseid}/${semesterToAbbr(value.semester)}`}>
                              {value.semester}
                            </Link>
                          )
                      }
                      extraClass={
                        `${this.props.colors.textMajorColor}`
                      }
                      dropdownContentsStyle={{}}
                    />
                  </span>
                }
                style={{backgroundColor: "rgba(255, 255, 255, 0.2)"}}
              />
            </h1>
            <h4 className={`light ${this.props.colors.textMajorColor}`}>{course.name}</h4>
            <p>
              {`/ ${course.department} /`}
              <br/>
              <br/>
              <br/>
              <br/>
              <br/>
            </p>
          </div>
          <div className="col s12 m5 offset-m1 offset-l2">
            Pre-requisites: {
              course.prereqs ? (
                <CoursesReqChips
                  requirements={course.prereqs}
                  colors={this.props.colors} />
              ) : (
                "None"
              )}
            <br/><br/>
          </div>
          <div className="col s12 m5">
            Co-requisites: {
              course.coreqs ? (
                <CoursesReqChips
                  requirements={course.coreqs}
                  colors={this.props.colors} />
              ) : (
                "None"
              )}
            <br/><br/>
          </div>
        </div>
        <div className="row">
          <div className="col s10 m5 offset-m1 offset-l2">
            Units: {course.units ? course.units.toFixed(1) : "Unknown"}
          </div>
        </div>
      </div>
    )
  }

  render() {
    return (
      <Card
        cardColor={this.props.colors.majorColor}
        extraClassName="hoverable"
        textColor={this.props.colors.textMajorColor}
        content={this.cardContent()}
      />
    );
  }
}

export default CoursesCard;
