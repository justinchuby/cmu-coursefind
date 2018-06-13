import React, { Component } from 'react';
// import { Link } from 'react-router-dom'

// let $ = window.jQuery = require('jquery');
const M = require('materialize-css/dist/js/materialize');

class SideNav extends Component {
  componentDidMount() {
    const elems = document.querySelectorAll('.sidenav');
    const instances = M.Sidenav.init(elems, {});
  }

  render() {
    return (
      <ul id="slide-out" className="sidenav">
        <li><a href="/" style={{fontSize: '150%'}}>Course Find</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/disclaimer">Disclaimer</a></li>
        <li><a href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank" rel="nofollow noopener noreferrer">Feedback</a></li>
      </ul>
    )
  }
}

export default SideNav;
