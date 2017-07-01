import React, { Component } from 'react';

class Footer extends Component {
  // left text, right text
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <footer className="page-footer blue-grey darken-1">
          <div className="container">
            <div className="row">
              <div className="col m5 s12">
                <span className="grey-text text-lighten-4 light">
                  { this.props.leftFooterText }
                </span>
              </div>
              <div className="col m7 s12">
                <span className="grey-text text-lighten-4 light right">
                  { this.props.rightFooterText }
                </span>
              </div>
            </div>
          </div>
          <div className="footer-copyright">
            <div className="container">
              <div className="row">
                <div className="col s5">
                  <a className="light grey-text text-lighten-1" href="/"> CMU Course Find </a>
                </div>
                <div className="col s7">
                  <div className="right">
                    <a className="light grey-text text-lighten-3" href="/">Home</a>
                    &nbsp;&nbsp;&nbsp;
                    <a className="light grey-text text-lighten-3" href="/about">About</a>
                    &nbsp;&nbsp;&nbsp;
                    <a className="light grey-text text-lighten-3" href="/disclaimer">Disclaimer</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    );
  }
}

export default Footer;
