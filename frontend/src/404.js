import React, { Component } from 'react';
import Layout from './components/Layout'
import { getCurrentSemester, searchTips } from './helpers'
import { Helmet } from 'react-helmet'


class NotFound extends Component {
  render() {
    return (
      <div>
        <Helmet>
          <title>{this.props.title || 'Not Found'} - CMU Course Find</title>
        </Helmet>
        <Layout
          navbarProps={{
            searchTips: searchTips
          }}
          mainContent={
            <div className="container">
              <div className="section">
                <div className="row container">
                  <div className="col s11">
                    <h3 className="grey-text text-darken-3">
                      {this.props.title || '404 Oops'}
                    </h3>
                    <br/>
                    <p className="grey-text text-darken-3 flow-text">
                      {this.props.message || 'Opps! The page disappears.'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          }
          footerProps={{
            leftFooterText: getCurrentSemester(),
            rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br /></span>
          }}
        />
      </div>
    )
  }
}

export default NotFound;
