// The main app. Routes are defined here
import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom'

import Home from './home'
import About from './about'
import Disclaimer from './disclaimer'


class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <Route exact path="/" component={Home}/>
          <Route path="/about" component={About}/>
          <Route path="/disclaimer" component={Disclaimer}/>
        </div>
      </Router>
    )
  }
}

export default App;
