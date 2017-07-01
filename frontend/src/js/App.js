import React, { Component } from 'react';
import CourseList from './components/CourseList'
import Navbar from './components/Navbar'
import SideNav from './components/SideNav'
import { Course } from './cmu_course'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: []
    }
  }

  componentWillMount() {
    // TODO: fix here
    fetch('https://api.cmucoursefind.xyz/course/v1/course/21-259/')
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        this.setState({
          courses: [new Course(jsonResponse.course)]
        })
      })
  }

  render() {
    return (
      <div>
        <Navbar />
        <SideNav />
      </div>
    )
  }
}

export default App;
