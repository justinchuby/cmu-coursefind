import React, { Component } from 'react';
import Navbar from './Navbar'
import SideNav from './SideNav'
import Footer from './Footer'
import '../styles/style.css';


class App extends Component {
  render() {
    return (
      <div className="flexbox-wrapper">
        <Navbar {...this.props.navbarProps} />
        <SideNav />
        <main className="container">
          {this.props.mainContent}
        </main>
        <Footer {...this.props.footerProps}/>
      </div>
    )
  }
}

export default App;
