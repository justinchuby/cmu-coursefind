import React, { Component } from 'react';
import CoursesCollapsibleElement from './CoursesCollapsibleElement'

var $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');

class CoursesCollapsible extends Component {
  componentDidMount() {
    // This would initialize all collapsibles but whatever
    $('.collapsible').collapsible();
  }

  render() {
    const collapsibleElements = this.props.list.map(
      (element, index) => {
        return (
          <CoursesCollapsibleElement
            key={element.key}
            leftHeaderIcon={element.leftHeaderIcon}
            leftHeaderText={element.leftHeaderText}
            rightHeaderText={element.rightHeaderText}
            rightHeaderTextShort={element.rightHeaderTextShort}
            bodyText={element.bodyText}
            first={index === 0}
            colorClass={`${this.props.colors.majorColor} ${this.props.colors.textMajorColor}`}
          />
        )
      }
    )
    return (
      <ul className={`collapsible ${this.props.extraClass}`}
        data-collapsible="accordion">
        {collapsibleElements}
      </ul>
    );
  }
}

export default CoursesCollapsible;
