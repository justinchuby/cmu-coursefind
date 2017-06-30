import React, { Component } from 'react';

class CollapsibleElement extends Component {
    constructor(props) {
    super(props);
  }

  render() {
    return (
      <li>
        <div className="collapsible-header waves-effect hoverable">
          {/* TODO: class options */}
          <div className="row nomargin">
            <div className="col s12 m8 l8 truncate">
              <i className="material-icons hide-on-small-only">class</i>
              <span>
                {this.props.leftHeaderText}
              </span>
            </div>
            <div className="col hide-on-small-only">
              <span className="right badge">
                {this.props.rightHeaderText}
              </span>
            </div>
            <div className="col s12 hide-on-med-and-up">
              <span className="right grey-text text-darken-1">
                {this.props.rightHeaderTextShort}
              </span>
            </div>
          </div>
        </div>
        <div className="collapsible-body blue-grey darken-1" style={{display: 'none'}}>
          {this.props.bodyText}
        </div>
      </li>
    );
  }
}

export default CollapsibleElement;
