import React, { Component } from 'react';
import CollapsibleElement from './CollapsibleElement'

var $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');

class Collapsible extends Component {
  // left text, right text
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    $('.collapsible').collapsible();
  }

  render() {
    let collapsibleElements = this.props.list.map(
      element => {
        return (
          <CollapsibleElement
            key={element.key}
            leftHeaderText={element.leftHeaderText}
            rightHeaderText={element.rightHeaderText}
            rightHeaderTextShort={element.rightHeaderTextShort}
            bodyText={element.bodyText}
          />
        )
      }
    )
    return (
      <ul className="collapsible" data-collapsible="accordion">
        {collapsibleElements}
      </ul>
    );
  }
}

export default Collapsible;
