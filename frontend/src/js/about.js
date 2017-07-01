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
  }

  render() {
    return (
      <div className="flexbox-wrapper">
        <Navbar />
        <SideNav />
        <main className="container">
          <p> This is about pageeee! </p>
        </main>
        <Footer
          leftFooterText={getSemesterFromDate(moment())}
          rightFooterText={<span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>}/>
      </div>
    )
  }
}

export default App;
