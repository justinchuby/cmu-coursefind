import React, { Component } from 'react';

class Chip extends Component {
  // props: content, extraClass
  render() {
    return (
      <div className={`chip ${this.props.extraClass}`}>
        {this.props.content}
      </div>
    )
  }
}

export default Chip;
