import React, { Component } from 'react';
import '../../css/Navbar.css';

var $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');

class Navbar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    /* TODO update search tip */
  return (
    <div className="navbar-fixed">
      <nav>
        <div className="nav-wrapper">
        <a data-activates="slide-out" className="button-collapse hide-on-med-and-up"><i className="material-icons">menu</i></a>
        <a href="/" className="brand-logo left hide-on-small-only light" id="brand-logo">&nbsp; Course Find</a>
        <div className="row" style={{height: '100%'}}>
          <form method="GET" action="/" className="col s8 m10 l11" id="search-box">
            <div className="input-field">
              <input type="search" name="q" className="field tooltipped"
              data-position="bottom" data-delay="300" data-tooltip="search_tip"
              required maxLength="100" placeholder="Search" id="search-text"/>
              <label className="label-icon" htmlFor="search-text"><i className="material-icons">search</i></label>
              <i className="material-icons">close</i>
            </div>
          </form>
          <ul className="right">
            <li><a><i className="material-icons">send</i></a></li>
          </ul>
        </div>
        </div>
      </nav>
    </div>
  );
  }
}

export default Navbar;
