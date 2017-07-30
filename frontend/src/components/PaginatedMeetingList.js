import React, { Component } from 'react';
import MeetingList from './MeetingList'
import Pagination from './Pagination'

class PaginatedMeetingList extends Component {
  // props: page, (page) size, meetings
  render() {
    const page = this.props.page
    const size = this.props.size
    if (size > 0) {
      const meetings = this.props.meetings.slice((page-1)*size, (page)*size)
      // Adjusted page number
      return (
        <div>
          <MeetingList meetings={meetings} />
          <br/><br/>
          <Pagination page={page} totalPage={Math.ceil(this.props.meetings.length/size)} />
        </div>
      )
    }
    return (
      null
    )
  }
}


export default PaginatedMeetingList;
