import React, { Component } from 'react';
import { Link, Redirect } from 'react-router-dom'
import { randomPick } from '../helpers';
import './Navbar.css';
import Spinner from './Spinner'


class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchPrompt: "Search",
      searchValue: props.searchValue || "",
      searchSubmitted: false,
    }
  }

  clearSearchBar(event) {
    this.setState({ searchValue: "" })
    event.target.blur()
  }

  handleChange(event) {
    this.setState({ searchValue: event.target.value })
  }

  handleSubmit(e) {
    e.preventDefault()
    this.setState({ searchSubmitted: true })
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

  componentDidUpdate() {
    if (this.state.searchSubmitted) {
      this.setState({ searchSubmitted: false })
    }
  }

  render() {
    if (this.state.searchSubmitted) {
      return <Redirect push to={{
        pathname: '/search',
        search: `?q=${this.state.searchValue}`
      }} />
    } else {
      return (
        <div className="navbar-fixed">
          <nav className={this.props.color}>
            <div className="nav-wrapper">
              <a
                data-target="slide-out"
                className="button-collapse hide-on-med-and-up sidenav-trigger">
                <i className="material-icons">menu</i>
              </a>
              <Link to="/"
                className="brand-logo left hide-on-small-only light"
                id="brand-logo">
                &nbsp; Course Find
              </Link>
              <div className="row" style={{ height: '100%' }}>
                <form
                  className="col s7 m10 l11"
                  id="search-box"
                  onSubmit={this.handleSubmit.bind(this)}>
                  <div className="input-field">
                    <input type="search" name="q" className="field"
                      required maxLength="100"
                      value={this.state.searchValue}
                      placeholder={this.state.searchPrompt}
                      id="search-text"
                      onFocus={this.handleFocus.bind(this)}
                      onBlur={this.handleBlur.bind(this)}
                      onChange={this.handleChange.bind(this)}></input>
                    <label className="label-icon" htmlFor="search-text">
                      {this.props.loader ? (
                        <Spinner />
                      ) : (
                          <i className="material-icons">search</i>
                        )}
                    </label>
                    <i className="material-icons"
                      onClick={this.clearSearchBar.bind(this)}>
                      close
                    </i>
                  </div>
                </form>
                <ul className="right">
                  <li>
                    <a onClick={this.handleSubmit.bind(this)}>
                      <i className="material-icons">send</i>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </nav>
        </div>
      );
    }
  }
}

export default Navbar;
