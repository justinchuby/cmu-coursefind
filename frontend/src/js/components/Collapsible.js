import React, { Component } from 'react';
import CollapsibleElement from './CollapsibleElement'

class Collapsible extends Component {
  // left text, right text
  constructor(props) {
    super(props);
  }

  render() {
    let collapsibleElements = this.props.list.map(
      element => {
        return (
          <CollapsibleElement
            leftHeaderText={element.leftHeaderText}
            rightHeaderText={element.rightHeaderText}
            rightHeaderTextShort={element.rightHeaderTextShort}
            bodyText={element.bodyText}
          />
        )
      }
    )
    return (
      <ul className="collapsible collapsible-accordion" data-collapsible="accordion">
        {collapsibleElements}
      </ul>
    );
  }
}

export default Collapsible;
