import React, { Component } from 'react';

class Card extends Component {
  // props: cardColor, extraClass, textColor, title, content
  render() {
    return (
      <div class={`card ${this.props.cardColor} ${this.props.extraClass}`}>
        <div class={`card-content ${this.props.textColor}`}>
          {this.props.title &&
            <span class="card-title">{this.props.title}</span>
          }
          {this.props.content}
        </div>
      </div>
    );
  }
}

export default Card;
