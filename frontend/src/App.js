// The main app. Routes are defined here
import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import './styles/style.css';

import Home from './home'
import About from './about'
import Disclaimer from './disclaimer'
import Courses from './courses'


class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/" component={Home}/>
          <Route path="/about" component={About}/>
          <Route path="/disclaimer" component={Disclaimer}/>
          <Route path="/courses/:courseid" component={Courses}/>
        </Switch>
      </Router>
    )
  }
}

export default App;
