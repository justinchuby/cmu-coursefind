import React, { Component } from 'react';
import CourseList from './components/CourseList'
import Navbar from './components/Navbar'
import SideNav from './components/SideNav'
import Footer from './components/Footer'
import { Course } from './cmu_course'
import { getSemesterFromDate } from './helpers'
import '../css/style.css';

var moment = require('moment');

class App extends Component {
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
    let searchTips = [
      "a course number '15-112'",
      "name of an instructor",
      "name of a course",
      "a room 'DH2210'",
      "a building 'Doherty'",
      "a time '8:00am'",
      "a day 'Monday'"
    ]
    return (
      <div className="flexbox-wrapper">
        <Navbar searchTips={searchTips} />
        <SideNav />
        <main>
          <CourseList courses={this.state.courses} />
        </main>
        <Footer
          leftFooterText={getSemesterFromDate(moment())}
          rightFooterText={<span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>}/>
      </div>
    )
  }
}

export default App;
