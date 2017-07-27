import React, { Component } from 'react'
import Layout from './components/Layout'
import MeetingList from './components/MeetingList'
import { Course } from './utils/cmu_course'
import { getSemesterFromDate, searchTips, currentISOTime } from './helpers'

var moment = require('moment');
let $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');

// import 'url-search-params-polyfill';
// const search = props.location.search; // could be '?foo=bar'
// const params = new URLSearchParams(search);
// const foo = params.get('foo'); // bar

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: [],
      lectures: [],
      sections: []
    }
  }

  componentDidMount() {
    $('ul.tabs').tabs();
  }

  componentWillMount() {
    fetch('https://api.cmucoursefind.xyz/course/v1/datetime/now/timespan/60/')
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        let courses = jsonResponse.courses.map(course => {return new Course(course)})
        this.setState({
          courses: courses,
          // get the lectures out from each course and reduce them from 2D
          // array to 1D array

          // TODO: write functions to filter and sort the sections before
          // display
          // make the sorting function flexible

          lectures: courses.map(
            course => {
              return course.lectures
            }).reduce(
            (a, b) => a.concat(b), []
            ),
          sections: courses.map(
            course => {
              return course.sections
            }).reduce(
            (a, b) => a.concat(b), []
            )
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
          (this.state.courses) ? (
            <div className="container">
              <div className="row">
                <div className="col s12">
                  <ul className="tabs">
                    <li className="tab col s3"><a href="#lec">Lectures</a></li>
                    <li className="tab col s3"><a href="#sec">Sections</a></li>
                  </ul>
                </div>
              </div>

              <div id="lec" className="row">
                <MeetingList meetings={this.state.lectures} />
              </div>
              <div id="sec" className="row">
                <MeetingList meetings={this.state.sections} />
              </div>

            </div>
          ) : (
            null
          )
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
