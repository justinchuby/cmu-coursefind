import React, { Component } from 'react';

class Pagination extends Component {
  // props: page, totalPage

  render() {
    const lis = [...Array(this.props.totalPage)].map((value, index) => {
      const page = index + 1
      return (
        <li key={index} className={`${page===this.props.page ? 'active' : 'waves-effect'}`}><a href={`#${page}`}>{page}</a></li>
      )
    })
    return (
      <ul className="pagination">
        <li className={`${this.props.page===1 ? 'disabled' : 'waves-effect'}`}>
          <a href={`#${
            (this.props.page > 1) ? (
            this.props.page-1
            ) : (
            this.props.page
            )}`}>
            <i className="material-icons">chevron_left</i>
          </a>
        </li>
        {lis}
        <li className={`${this.props.page===this.props.totalPage ? 'disabled' : 'waves-effect'}`}>
          <a href={`#${
            (this.props.page < this.props.totalPage) ? (
            this.props.page+1
            ) : (
            this.props.page
            )}`}>
            <i className="material-icons">chevron_right</i>
          </a>
        </li>
      </ul>
    )
  }
}

export default Pagination;
