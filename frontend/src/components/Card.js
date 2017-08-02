import React, { Component } from 'react';

class Card extends Component {
  // props: cardColor, extraClass, textColor, title, content
  render() {
    return (
      <div className={`card ${this.props.cardColor} ${this.props.extraClass}`}>
        <div className={`card-content ${this.props.textColor}`}>
          {this.props.title &&
            <span className="card-title">{this.props.title}</span>
          }
          {this.props.content}
        </div>
      </div>
    );
  }
}

export default Card;
