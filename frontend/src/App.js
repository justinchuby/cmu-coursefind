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
import Search from './search'


class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/" component={Home}/>
          <Route exact path="/about" component={About}/>
          <Route exact path="/disclaimer" component={Disclaimer}/>
          <Route exact path="/courses/:courseid(\d{2}-\d{3})" component={Courses}/>
          <Route exact path="/courses/:courseid(\d{2}-\d{3})/:term" component={Courses}/>
          {/* TODO: display the search query text on search box when access from url  */}
          <Route exact path="/search" component={Search}/>
        </Switch>
      </Router>
    )
  }
}

export default App;
