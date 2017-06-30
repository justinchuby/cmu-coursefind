import React, { Component } from 'react';
import logo from '../img/logo.svg';
import '../css/App.css';
import Collapsible from './components/Collapsible'

class App extends Component {
  render() {
    let list = [{
      leftHeaderText: "left",
      rightHeaderText: "right",
      rightHeaderTextShort: "short",
      bodyText: "bodyyyy"
    }]
    return (
      <Collapsible list={list}/>
    )
  }
}

export default App;
