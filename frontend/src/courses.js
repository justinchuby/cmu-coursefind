import React, { Component } from 'react'
import { Helmet } from 'react-helmet'
import { Redirect } from 'react-router-dom'
import Layout from './components/Layout'
import CoursesCard from './components/CoursesCard'
import CoursesDescription from './components/CoursesDescription'
import CoursesLectureCards from './components/CoursesLectureCards'
import CoursesSectionList from './components/CoursesSectionList'
import CoursesInstructorChips from './components/CoursesInstructorChips'
import { Course } from './utils/cmu_course'
import {
  searchTips,
  getCurrentSemester,
  compareSemesters,
  semesterFromAbbr
} from './helpers'
import { getDetailPageColor } from './utils/detailsPageColor'
import NotFound from './404'

class Courses extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courses: {},
      semester: null,
      colors: {
        majorColor: 'purple lighten-1',
        textMajorColor: 'white-text',
        courseidColor: 'purple-text text-darken-4',
        titleColor: 'purple-text text-darken-3',
        textAccentColor: 'teal-text text-accent-2',
        NavbarColor: ''
      },
      response: {},
      loaded: false
    }
  }

  displayCourse(props, courses) {
    if (courses.length === 0) {
      throw new Error('displayCourse: Courses must have a length of more than 0')
    }
    let courseObjs = {}
    for (let course of courses) {
      // Use semester as key
      courseObjs[course.semester] = new Course(course)
    }
    let semester
    if (props.match.params.semester) {
      semester = semesterFromAbbr(props.match.params.semester)
    } else {
      semester = pickSemesterFromCourses(courseObjs)
    }
    this.setState({
      courses: courseObjs,
      semester: semester,
      colors: getDetailPageColor(props.match.params.courseid),
      loaded: true
    })
  }

  componentWillMount() {
    this.componentWillReceiveProps(this.props)
  }

  componentDidMount() {
    let elems = document.getElementsByClassName("plain-text")
    if (elems.length !== 0) {
      for (let i = 0; i < elems.length; i++) {
        elems[i].style.cssText = "display: none;"
      }
    }
  }

  componentWillReceiveProps(nextProps) {
    let url = `https://api.cmucoursefind.xyz/course/v1/courseid/${nextProps.match.params.courseid}/`
    fetch(url)
      .then((response) => {
        this.setState({response: response})
        if (response.ok) {
          // A course is found
          return response.json()
        }
        return {}
      })
      .then((jsonResponse) => {
        if (jsonResponse.courses && jsonResponse.courses.length !== 0) {
          this.displayCourse(nextProps, jsonResponse.courses)
        }
      })
  }

  render() {
    if (this.state.response.status === 404) {
      // No information about the course
      return (
        <NotFound message={
          <span>
          We don't have information about the course {this.props.match.params.courseid} for now. 
          If you think this is an error, please 
          <a href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank" rel="nofollow noopener noreferrer"> report it</a>
          . Thanks!
          </span>
        }/>
      )
    }
    const selectedCourse = this.state.courses[this.state.semester]
    if (this.state.loaded && !selectedCourse) {
      // No information about the requested semester
      return (
        <Redirect push to={{
          pathname: `/courses/${this.props.match.params.courseid}`
          }}
        />
      )
    }
    return (
      <div>
        <Helmet>
          {selectedCourse && (
            <title>{selectedCourse.courseid}: {selectedCourse.name} - {selectedCourse.semester} - CMU Course Find</title>
          )}
          {selectedCourse && (
            <meta name="description" content={`${selectedCourse.courseid}: ${selectedCourse.name}.  ${selectedCourse.desc}`} />
          )}
        </Helmet>
        <Layout
          navbarProps={{
            searchTips: searchTips,
            color: this.state.colors.NavbarColor
          }}
          mainContent={
            (selectedCourse) ? (
              /* course loaded */
              <div>
                <div className="row">
                  <div className="col s12 l9">
                    <CoursesCard
                      courses={this.state.courses}
                      semester={this.state.semester}
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
                        <CoursesDescription content={selectedCourse.desc} />
                      </div>
                    </div>
                  </div>
                  <div className="section">
                    <h4>Instructors</h4>
                    <br />
                    <div className="row">
                      <div className="col s12 m10">
                        <CoursesInstructorChips
                          instructors={selectedCourse.instructors} />
                      </div>
                    </div>
                  </div>
                  {
                    (selectedCourse.lectures.length !== 0) ? (
                      <div className="section">
                        <h4>Lectures</h4>
                        <br />
                        <CoursesLectureCards
                          meetings={selectedCourse.lectures}
                          colors={this.state.colors}
                        />
                      </div>
                    ) : (
                        null
                      )
                  }
                  {
                    (selectedCourse.sections.length !== 0) ? (
                      <div className="section">
                        <h4>Sections</h4>
                        <br />
                        <CoursesSectionList
                          meetings={selectedCourse.sections}
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
            leftFooterText: selectedCourse ? selectedCourse.semester : '',
            rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank" rel="nofollow noopener noreferrer">send me feedbacks !</a><br /></span>
          }}
        />
      </div>
    )
  }
}

export default Courses;

function pickSemesterFromCourses(courses) {
  // todo check this
  const currentSemester = getCurrentSemester()
  if (courses.hasOwnProperty(currentSemester)) {
    return currentSemester
  }
  
  const sortedCourses = [...Object.values(courses)]
    .sort((a, b) => compareSemesters(a.semester, b.semester))
    .reverse()
  return sortedCourses[0].semester
}
