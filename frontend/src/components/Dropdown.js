import React, { Component } from 'react';

class Dropdown extends Component {
  // props: name, content, dropdownContents, extraClasses
  render() {
    const dropdownContents = this.props.dropdownContents.map((elem, index) => {
      return (
        <li key={index}>{elem}</li>
      )
    })
    return (
      <span>
        <a class={`dropdown-button ${...extraClasses}`} href='#' data-activates={this.props.name}>{this.props.content}</a>
        <ul id={this.props.name} class='dropdown-content'>
          {dropdownContents}
        </ul>
      </span>
    )
  }
}

export default Dropdown;
