import React, { Component } from 'react'
import Layout from './components/Layout'
import MeetingList from './components/MeetingList'
import { Course } from './utils/cmu_course'
import { Helmet } from 'react-helmet'
import {
  getCurrentSemester,
  searchTips,
  getMini
} from './helpers'

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
      courses: null,
      lectures: null,
      sections: null,
      tick: false
    }
  }

  componentWillMount() {
    fetch('https://api.cmucoursefind.xyz/course/v1/datetime/now/timespan/60/?filtered_fields=desc')
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        let courses = jsonResponse.courses.map(course => { return new Course(course) }) || []
        // Makes sure courses is an array
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
            ).filter(
            meeting => {
              return filterMeeting(meeting)
            }
            ),
          sections: courses.map(
            course => {
              return course.sections
            }).reduce(
            (a, b) => a.concat(b), []
            ).filter(
            meeting => {
              return filterMeeting(meeting)
            }
            )
        })
      })
  }

  componentDidMount() {
    $('ul.tabs').tabs();
    this.interval = setInterval(() => this.tick(), 60000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  tick() {
    // Rerender the page every minute
    this.setState({ tick: !this.state.tick })
  }

  render() {
    return (
      <div>
        <Helmet>
          <title>CMU Course Find</title>
          <meta name="description" content="A better course finder for Carnegie Mellon University. Course description, schedule, instructor info, etc. See classes that are happening and discover new courses!" />
        </Helmet>
        <Layout
          navbarProps={{
            searchTips: searchTips
          }}
          mainContent={
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
                {(this.state.lectures) ? (
                  (this.state.lectures.length !== 0) ? (
                    // some lectures are happening now
                    <div className="col s12">
                      <p className="flow-text grey-text text-darken-1">
                        There are currently {this.state.lectures.length} lectures.
                        </p>
                      <MeetingList meetings={this.state.lectures} />
                    </div>
                  ) : (
                      // no lectures now
                      <div className="col s12">
                        <p className="flow-text grey-text text-darken-1">
                          No lectures happening at this time. Take a break :D
                        </p>
                      </div>
                    )
                ) : (
                    // courses not loaded
                    null
                  )
                }
              </div>
              <div id="sec" className="row">
                {(this.state.sections) ? (
                  (this.state.sections.length !== 0) ? (
                    <div className="col s12">
                      <p className="flow-text grey-text text-darken-1">
                        There are currently {this.state.sections.length} sections.
                      </p>
                      <MeetingList meetings={this.state.sections} />
                    </div>
                  ) : (
                      <div className="col s12">
                        <p className="flow-text grey-text text-darken-1">
                          No sections happening at this time. Take a break :D
                      </p>
                      </div>
                    )
                ) : (
                    null
                  )
                }
              </div>
            </div>
          }
          footerProps={{
            leftFooterText: getCurrentSemester(),
            rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br /></span>
          }}
        />
      </div>
    )
  }
}

function filterMeeting(meeting) {
  if (!meeting.isHappeningNow() && !meeting.willHappenIn(60)) {
    // Will not happen in an hour & not happening now
    return false
  }
  if (meeting.location !== 'Pittsburgh, Pennsylvania') {
    return false
  }
  if (meeting.course.mini !== 0 && meeting.course.mini !== getMini()) {
    // Not the correct mini
    return false
  }
  return true
}

export default Home;
