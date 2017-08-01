import React, { Component } from 'react';
import Layout from './components/Layout'
import { getCurrentSemester, searchTips } from './helpers'
import { Helmet } from 'react-helmet'


class NotFound extends Component {
  render() {
    return (
      <div>
        <Helmet>
          <title>Not Found - CMU Course Find</title>
        </Helmet>
        <Layout
          navbarProps={{
            searchTips: searchTips
          }}
          mainContent={
            <div className="container">
              <div class="section white">
                <div class="row container">
                  <div class="col s11">
                  <h4 class="grey-text text-darken-3">
                    404<br/><br/>
                    {this.props.message || 'Opps! The page disappears.'}</h4>
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
