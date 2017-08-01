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
      }
    }
  }

  displayCourse(props, courses) {
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
      // TODO: get a better name for this function
      semester: semester,
      colors: getDetailPageColor(props.match.params.courseid)
    })
  }

  componentWillMount() {
    this.componentWillReceiveProps(this.props)
  }

  componentWillReceiveProps(nextProps) {
    let url = `https://api.cmucoursefind.xyz/course/v1/courseid/${nextProps.match.params.courseid}/`
    fetch(url)
      .then((response) => { return response.json() })
      .then((jsonResponse) => {
        if (jsonResponse.courses) {
          this.displayCourse(nextProps, jsonResponse.courses)
          // jsonResponse.courses.length !== 0
          // TODO: check response status code and decide if 404
        }
        // TODO: deal with the case when there's a server error
        // TODO: deal with 404's
      })
  }

  render() {
    const selectedCourse = this.state.courses[this.state.semester]
    if (!selectedCourse && Object.keys(this.state.courses).length !== 0) {
      // No information about the requested semester
      return (
        <Redirect push to={{
          pathname: `/courses/${this.props.match.params.courseid}`
          }}
        />
      )
    }
    if (Object.keys(this.state.courses).length === 0) {
      // No information about the course
      return (
        <NotFound message={
          `We can't find ${this.props.match.params.courseid} for now. 
          If you think this is an error, please ${<a href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">report it</a>}. Thanks!`
        }/>
      )
    }
    return (
      <div>
        <Helmet>
          {selectedCourse && (
            <title>{selectedCourse.courseid}: {selectedCourse.name} - {selectedCourse.semester} - CMU Course Find</title>
          )}
          {selectedCourse && (
            <meta name="description" content={`${selectedCourse.courseid}: ${selectedCourse.name}  ${selectedCourse.desc}`} />
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
            rightFooterText: <span>Please <a className="teal-text text-accent-1" href="http://www.google.com/recaptcha/mailhide/d?k=01wipM4Cpr-h45UvtXdN2QKQ==&c=r0MIa1Nhtz6i9zAotzfExghYzS_a8HaYrmn_MGl-GBE=" target="_blank">send me feedbacks !</a><br /></span>
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
