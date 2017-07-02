import React, { Component } from 'react';
import { randomPick } from '../helpers';
import '../../css/Navbar.css';


class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchPrompt: "Search"
    }
  }

  handleFocus(e) {
    this.setState({
      searchPrompt: randomPick(this.props.searchTips)
    })  
  }

  handleBlur(e) {
    this.setState({
      searchPrompt: "Search"
    })  
  }

  render() {
    return (
      <div className="navbar-fixed" style={{height: '100px'}}>
        <nav>
          <div className="nav-wrapper">
            <a data-activates="slide-out" className="button-collapse hide-on-med-and-up"><i className="material-icons">menu</i></a>
            <a href="/" className="brand-logo left hide-on-small-only light" id="brand-logo">&nbsp; Course Find</a>
            <div className="row" style={{ height: '100%' }}>
              <form method="GET" action="/" className="col s8 m10 l11" id="search-box">
                <div className="input-field">
                  <input type="search" name="q" className="field"
                    required maxLength="100" placeholder={this.state.searchPrompt} id="search-text" 
                    onFocus={this.handleFocus.bind(this)}
                    onBlur={this.handleBlur.bind(this)}></input>
                  <label className="label-icon" htmlFor="search-text"><i className="material-icons">search</i></label>
                  <i className="material-icons">close</i>
                </div>
              </form>
              <ul className="right">
                <li><a><i className="material-icons">send</i></a></li>
              </ul>
            </div>
          </div>
        </nav>
      </div>
    );
  }
}

export default Navbar;
