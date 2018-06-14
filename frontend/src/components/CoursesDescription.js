import React, { Component } from 'react'
import Linkify from 'linkifyjs/react';

// const sanitizeHtml = require('sanitize-html')
const $ = require('jquery')
require('../utils/readmore')

class CoursesDescription extends Component {
  // props: content
  componentDidMount() {
    $('.readmore').readmore();
  }

  render() {
    return (
      this.props.content ? (
        // <p className="grey-text text-darken-3 readmore"
        //   dangerouslySetInnerHTML={{__html: this.props.content}}>
        <p className="grey-text text-darken-3 readmore">
          <Linkify>
            {this.props.content}
          </Linkify>
        </p>
      ) : (
        <p className="grey-text text-darken-3">
          No description available.
        </p>
      )
    );
  }
}

export default CoursesDescription;
