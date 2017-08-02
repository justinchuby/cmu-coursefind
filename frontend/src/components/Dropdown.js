import React, { Component } from 'react';

var $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');

class Dropdown extends Component {
  // props: name, content, dropdownContents, extraClass
  componentDidMount() {
    $('.dropdown-button').dropdown({
        inDuration: 300,
        outDuration: 225,
        constrainWidth: false, // Does not change width of dropdown to that of the activator
        hover: false, // Activate on hover
        gutter: 0, // Spacing from edge
        belowOrigin: false, // Displays dropdown below the button
        alignment: 'left', // Displays dropdown with edge aligned to the left of button
        stopPropagation: false // Stops event propagation
      }
    );
  }

  render() {
    const dropdownContents = this.props.dropdownContents.map((elem, index) => {
      return (
        <li key={index}>{elem}</li>
      )
    })
    return (
      <span>
        <a
          className={`dropdown-button ${this.props.extraClass}`}
          data-activates={this.props.name}>
          {this.props.content}
        </a>
        <ul
          id={this.props.name}
          className='dropdown-content'
          style={this.props.dropdownContentsStyle}>
          {dropdownContents}
        </ul>
      </span>
    )
  }
}

export default Dropdown;
