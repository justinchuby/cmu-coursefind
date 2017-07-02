import React, { Component } from 'react';

class Card extends Component {
  render() {
    return (
      <div class={`card ${this.props.cardColor} ${this.props.extraProps.join(" ")}`}>
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
