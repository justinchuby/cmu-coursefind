import React, { Component } from 'react';

class CourseCollapsibleElement extends Component {
  render() {
    return (
      <li>
        <div className={`collapsible-header waves-effect hoverable ${this.props.first && "active"}`}>
          <div className="row nomargin">
            <div className="col s5">
              {this.props.leftHeaderIcon}
              <span>
                {this.props.leftHeaderText}
              </span>
            </div>
            <div className="col s7">
              <p class="light right-align truncate nomargin">
                {this.props.rightHeaderText}
              </p>
            </div>
          </div>
        </div>
        <div className={`collapsible-body ${this.props.colors}.join(" ")`}>
          {this.props.bodyText}
        </div>
      </li>
    );
  }
}

export default CourseCollapsibleElement;
