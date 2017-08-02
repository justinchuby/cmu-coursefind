import React, { Component } from 'react';
import CollapsibleElement from './CollapsibleElement'

var $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');

class Collapsible extends Component {
  componentDidMount() {
    // This would initialize all collapsibles but whatever
    $('.collapsible').collapsible();
  }

  render() {
    const collapsibleElements = this.props.list.map(
      element => {
        return (
          <CollapsibleElement
            key={element.key}
            leftHeaderIcon={element.leftHeaderIcon}
            leftHeaderText={element.leftHeaderText}
            rightHeaderText={element.rightHeaderText}
            rightHeaderTextShort={element.rightHeaderTextShort}
            bodyText={element.bodyText}
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

export default Collapsible;
