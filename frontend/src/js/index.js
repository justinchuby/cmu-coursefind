import React from 'react';
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom'
import registerServiceWorker from './registerServiceWorker';
// import '../css/index.css';
import App from './App';
import About from './about'


ReactDOM.render((
  <Router>
    <div>
      <Route exact path="/" component={App}/>
      <Route path="/about" component={About}/>
    </div>
  </Router>
), document.getElementById('root'))

registerServiceWorker();
