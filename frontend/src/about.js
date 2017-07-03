import React, { Component } from 'react';
import Layout from './components/Layout'
import { getSemesterFromDate, searchTips } from './helpers'

var moment = require('moment');

class About extends Component {
  render() {
    const mainText = (
      <div className="container">
        <div className="row">
          <div className="col s11">
          <h2 className="light">Hi !</h2>
          <h4 className="grey-text text-darken-3">About CMU Course Find</h4>
          <p className="grey-text text-darken-2">
            <br />
            CMU Course Find was a 15-112 term project by Justin Chu (me) during the Fall 2015 semester at Carnegie Mellon University. It is still an on going project. This site is proudly using <a href="https://scottylabs.org/course-api/" target="_blank" rel="nofollow">Course API by ScottyLabs</a>, and also <a href="http://materializecss.com" className="grey-text text-darken-3" target="_blank" rel="nofollow">Materialize</a>, a CSS Framework by CMU students.
            <br /><br />
            I had this idea one day when I was wandering in Wean Hall. I saw students having class and hoped to find out what class they were having. I could just walk in and see what was going on, but it would be much better if I knew something about the class.
            <br /><br />
            CMU Course Find makes it easier for you to figure out what’s going on in a class room. You can also see <b>what’s happening</b> at a particular time, so you can <b>go and discover</b> courses that interest you. This web app is also great for finding the room for a class, or just browsing the catalog to see what’s interesting.
            <br /><br />
            To find a course, you may search for the name of a course, name of instructors, name of a building, number of a course, or a room number. You can further view course reviews on <a href="http://cmucoursereviews.me" className="grey-text text-darken-3" target="_blank" rel="nofollow">cmucoursereviews.me</a>, also a 112 term project by Amit Nambiar.
            <br /><br />
            If you have any suggestion or if you would like to contribute to this project, please don’t hesitate to <a href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&amp;c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank" onClick={(e) => {e.preventDefault(); window.open('http://www.google.com/recaptcha/mailhide/d?k\x3d01wipM4Cpr-h45UvtXdN2QKQ\x3d\x3d\x26c\x3dr0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE\x3d', '', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width=500,height=300'); return false;}} title="Reveal this e-mail address">email me!</a>
            <br /><br /><br />
            Happy learning!
            <br />
            Justin
            <br /><br /><br />
            - This site is mobile-friendly. <b>Pin it to your home screen!</b>
            <br />
            - Watch the introduction video on <a href="https://youtu.be/QzxAUsKCtxM" target="_blank" rel="nofollow">Youtube</a>
          </p>
          </div>
        </div>
      </div>
    )
    return (
      <Layout
        navbarProps={{
          searchTips: searchTips
        }}
        mainContent={mainText}
        footerProps={{
          leftFooterText: getSemesterFromDate(moment()),
          rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>
        }}
      />
    )
  }
}

export default About;
