import React, { Component } from 'react'
import ReadMore from 'react-readmore';

const sanitizeHtml = require('sanitize-html')

class CoursesDescription extends Component {
  // props: content
  componentDidMount() {
    // This would initialize all collapsibles but whatever
    $('.collapsible').collapsible();
  }

  render() {
    return (
      content ? (
        <ReadMore>
          <p className="grey-text text-darken-3 readmore"
            dangerouslySetInnerHTML={{__html: sanitizeHtml(this.props.content)}}>
            {/* TODO: add target_blank to the urls */}
          </p>
        </ReadMore>
      ) : (
        <p className="grey-text text-darken-3">
          No description available.
        </p>
      )
    );
  }
}

export default CoursesDescription;
