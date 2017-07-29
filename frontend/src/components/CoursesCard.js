import React, { Component } from 'react';
import Card from './Card'
import CoursesReqChips from './CoursesReqChips'

class CoursesCard extends Component {
  // props: course, colors:{majorColor, textMajorColor, courseidColor, textAccentColor}
  // TODO: consider store the colors into a sigle object
  cardContent() {
    const course = this.props.course
    return (
      <div className="row">
        <div className="col m9 offset-m1 offset-l2">
          <h1 className={`light ${this.props.colors.courseidColor}`}>
            {course.courseid}
            <span className="hide-on-small-only flow-text"> {course.semester}</span>
          </h1>
          <p className={`hide-on-med-and-up flow-text ${this.props.colors.textMajorColor}`}>
            {course.semester}
          </p>
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
        <div className="col s10 m5 offset-m1 offset-l2">
          Units: {course.units ? course.units.toFixed(1) : "Unknown"}
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
