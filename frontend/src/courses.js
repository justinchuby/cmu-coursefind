import React, { Component } from 'react'
import Layout from './components/Layout'
import CoursesCard from './components/CoursesCard'
import CoursesDescription from './components/CoursesDescription'
import CoursesLectureCards from './components/CoursesLectureCards'
import CoursesSectionList from './components/CoursesSectionList'
import CoursesInstructorChips from './components/CoursesInstructorChips'
import { Course } from './utils/cmu_course'
import { searchTips } from './helpers'
import { getDetailPageColor } from './utils/detailsPageColor'


class Courses extends Component {
  constructor(props) {
    super(props);
    this.state = {
      course: null,
      colors: {
        majorColor: 'purple lighten-1',
        textMajorColor: 'white-text',
        courseidColor: 'purple-text text-darken-4',
        titleColor: 'purple-text text-darken-3',
        textAccentColor: 'teal-text text-accent-2',
        NavbarColor: ''
      }
    }
  }

  displayCourse(courses) {
    let courseObj = new Course(courses[0])
    // TODO: add button to switch between courses
    this.setState({
      course: courseObj,
      colors: getDetailPageColor(courseObj.courseid)
    })
  }

  componentDidMount() {
    let url = `https://api.cmucoursefind.xyz/course/v1/courseid/${this.props.match.params.courseid}/`
    fetch(url)
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        if (jsonResponse.courses) {
          this.displayCourse(jsonResponse.courses)
        }
        // TODO: deal with the case when there's a server error
        // TODO: deal with 404's
      })
  }

  render() {
    return (
      <Layout
        navbarProps={{
          searchTips: searchTips,
          color: this.state.colors.NavbarColor
        }}
        mainContent={
          (this.state.course) ? (
            /* course loaded */
            <div>
              <div className="row">
                <div className="col s12 l9">
                  <CoursesCard
                    course={this.state.course}
                    colors={this.state.colors}
                  />
                </div>
              </div>
              <div className="container">
                <div className="section">
                  <h4>Description</h4>
                  <br />
                  <div className="row">
                    <div className="col s12 m10">
                      <CoursesDescription content={this.state.course.desc}/>
                    </div>
                  </div>
                </div>
                 <div className="section">
                  <h4>Instructors</h4>
                  <br />
                  <div className="row">
                    <div className="col s12 m10">
                      
                      <CoursesInstructorChips
                        instructors={this.state.course.instructors} />
                    </div>
                  </div>
                </div>
                {
                  (this.state.course.lectures.length !== 0) ? (
                    <div className="section">
                      <h4>Lectures</h4>
                      <br />
                      <CoursesLectureCards 
                        meetings={this.state.course.lectures}
                        colors={this.state.colors}
                      />
                    </div>
                  ) : (
                    null
                  )
                }
                {
                  (this.state.course.sections.length !== 0) ? (
                    <div className="section">
                      <h4>Sections</h4>
                      <br />
                      <CoursesSectionList 
                        meetings={this.state.course.sections}
                        colors={this.state.colors}
                      />
                    </div>
                  ) : (
                    null
                  )
                }
                <div className="section">
                  <h4>Ratings</h4>
                  <br />
                </div>
              </div>
            </div>
          ) : (
            null
          )
        }
        footerProps={{
          leftFooterText: this.state.course ? this.state.course.semester : '',
          rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br/></span>
        }}
      />
    )
  }
}

export default Courses;
