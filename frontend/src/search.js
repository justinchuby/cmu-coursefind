import React, { Component } from 'react'
import Layout from './components/Layout'
import MeetingList from './components/MeetingList'
import Spinner from './components/Spinner'
import { Course } from './utils/cmu_course'
import {
  getCurrentSemester,
  searchTips} from './helpers'
import 'url-search-params-polyfill';

let $ = window.jQuery = require('jquery');
require('materialize-css/dist/js/materialize');


class Search extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: null,
      lectures: null,
      sections: null,
      query: null,
      loading: false
    }
  }

  componentDidMount() {
    $('ul.tabs').tabs();
  }

  componentWillMount() {
    this.componentWillReceiveProps(this.props)
  }

  componentWillReceiveProps(nextProps) {
    const search = nextProps.location.search; // could be '?foo=bar'
    const params = new URLSearchParams(search);
    const query = params.get('q');
    this.setState({query: query, loading: true})
    // const parsedQuery = parseQuery(query)
    // TODO: parse query
    // TODO: how do I refresh the query string when it changes?
    // TODO: fix fetch
    fetch(`https://api.cmucoursefind.xyz/course/v1/search/?text=${query}`)
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        let courses = jsonResponse.courses.map(course => {return new Course(course)}) || []
        // Makes sure courses is an array
        this.setState({
          courses: courses,
          // get the lectures out from each course and reduce them from 2D
          // array to 1D array

          // TODO: write functions to filter and sort the sections before
          // display
          // make the sorting function flexible

          lectures: courses.map(
            course => {
              return course.lectures
            }).reduce(
              (a, b) => a.concat(b), []
            ),
          sections: courses.map(
            course => {
              return course.sections
            }).reduce(
              (a, b) => a.concat(b), []
            ),
          loading: false
        })
      })
  }

  render() {
    return (
      <Layout
        navbarProps={{
          searchTips: searchTips,
          searchValue: this.state.query
        }}
        mainContent={
          <div className="container">
            <div className="row">
              <div className="col s12">
                <ul className="tabs">
                  <li className="tab col s3"><a href="#lec">Lectures</a></li>
                  <li className="tab col s3"><a href="#sec">Sections</a></li>
                </ul>
              </div>
            </div>

            <div id="lec" className="row">
              {
                (!this.state.loading) ? (
                  (this.state.lectures.length !== 0) ? (
                    <div>
                      <p className="flow-text grey-text text-darken-1">
                        Found {this.state.lectures.length} lectures.
                      </p> 
                      <MeetingList meetings={this.state.lectures} />
                    </div>
                  ) : (
                    <div>
                      <p className="flow-text grey-text text-darken-1">
                        No lectures were found. Try something else!
                      </p>
                    </div>
                  )
                ) : (
                  <Spinner />
                )
              }
            </div>
            <div id="sec" className="row">
              {
                (!this.state.loading) ? (
                  (this.state.sections.length !== 0) ? (
                    <div>
                      <p className="flow-text grey-text text-darken-1">
                        Found {this.state.sections.length} sections.
                      </p> 
                      <MeetingList meetings={this.state.sections} />
                    </div>
                  ) : (
                    <div>
                      <p className="flow-text grey-text text-darken-1">
                        No sections were found. Try something else!
                      </p>
                    </div>
                  )
                ) : (
                  <Spinner />
                )
              }
            </div>
          </div>
        }
        footerProps={{
          leftFooterText: getCurrentSemester(),
          rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>
        }}
      />
    )
  }
}

export default Search;
