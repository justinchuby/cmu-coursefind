import React, { Component } from 'react'
import Layout from './components/Layout'
import CoursesCard from './components/CoursesCard'
import { Course } from './cmu_course'
import { searchTips } from './helpers'

var moment = require('moment');

class Courses extends Component {
  constructor(props) {
    super(props);
    this.state = {
      course: {}
    }
  }

  componentWillMount() {
    console.log(this.props.params)
    fetch(`https://api.cmucoursefind.xyz/course/v1/course/${this.props.match.params.courseid}/`)
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
    const colors = {
      majorColor: 'purple lighten-1',
      textMajorColor: 'white-text',
      courseidColor: 'purple-text text-darken-4',
      titleColor: 'purple-text text-darken-3',
      textAccentcolor: 'teal-text text-accent-2'
    }
    return (
      <Layout
        navbarProps={{
          searchTips: searchTips
        }}
        mainContent={
          <CoursesCard
            course={this.state.course}
            colors={colors}
          />
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
