import React, { Component } from 'react'
import Layout from './components/Layout'
import CourseList from './components/CourseList'
import { Course } from './cmu_course'
import { getSemesterFromDate, searchTips } from './helpers'

var moment = require('moment');

// import 'url-search-params-polyfill';
// const search = props.location.search; // could be '?foo=bar'
// const params = new URLSearchParams(search);
// const foo = params.get('foo'); // bar

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: []
    }
  }

  componentWillMount() {
    // TODO: fix here
    // fetch('https://api.cmucoursefind.xyz/course/v1/building/dh/room/2315/')
    fetch('https://api.cmucoursefind.xyz/course/v1/instructor/david%20kosbie/')
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        this.setState({
          courses: jsonResponse.courses.map(course => {return new Course(course)})
        })
      })
  }

  render() {
    return (
      <Layout
        navbarProps={{
          searchTips: searchTips
        }}
        mainContent={
          <div className="container">
            <CourseList courses={this.state.courses} />
          </div>
        }
        footerProps={{
          leftFooterText: getSemesterFromDate(moment()),
          rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>
        }}
      />
    )
  }
}

export default Home;
