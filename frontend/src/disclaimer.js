import React, { Component } from 'react';
import Layout from './components/Layout'
import { getCurrentSemester, searchTips } from './helpers'
import { Helmet } from 'react-helmet'


class Disclaimer extends Component {
  render() {
    const mainText = (
      <div className="container">
        <div className="row">
          <div className="col s11">
            <h2 className="light">Disclaimer</h2>
            <p className="grey-text text-darken-3">
              <br />
              All course information provided through this site ("Content") is
              obtained from Carnegie Mellon University’s “Schedule of Classes” on
              <a href="https://enr-apps.as.cmu.edu/open/SOC/SOCServlet" target="_blank" rel="nofollow"> https://enr-apps.as.cmu.edu/open/SOC/SOCServlet </a>.
              The operators of this site are not responsible for the accuracy of the information provided through this site.
              Under no circumstances will this site or its operators be liable in any way for any Content, including, but not limited to, any errors or omissions in any Content, or any loss or damage of any kind incurred as a result of the use of any Content posted, emailed, transmitted or otherwise made available via this site or broadcast elsewhere.
              For up-to-date information, please refer to the Schedule of Classes.
            </p>
          </div>
        </div>
      </div>
    )
    return (
      <div>
        <Helmet>
          <meta charSet="utf-8" />
          <title>Disclaimer - CMU Course Find</title>
        </Helmet>
        <Layout
          navbarProps={{
              searchTips: searchTips
            }}
          mainContent={mainText}
          footerProps={{
            leftFooterText: getCurrentSemester(),
            rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>
          }}
        />
      </div>
    )
  }
}

export default Disclaimer;
