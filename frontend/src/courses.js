import React, { Component } from 'react'
import Layout from './components/Layout'
import CoursesCard from './components/CoursesCard'
import { Course } from './cmu_course'
import { getSemesterFromDate, searchTips } from './helpers'
import parseURL from './utils/parseURL'

var moment = require('moment');

class Courses extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courseid: ,
      course: {}
    }
  }

  componentWillMount() {
    fetch(`https://api.cmucoursefind.xyz/course/v1/course/${this.params.courseid}/`)
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        if (jsonResponse.course !== null) {
          this.setState({
            course: new Course(jsonResponse.course)
          })
        }
        // TODO: deal with the case when there's a server error
        // TODO: deal with 404's
      })
  }

  render() {
    return (
      <Layout
        navbarProps={{
          searchTips: searchTips
        }}
        mainContent={
          <CoursesCard course={this.state.course} />
        }
        footerProps={{
          leftFooterText: this.state.course.semester,
          rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>
        }}
      />
    )
  }
}

export default Courses;
