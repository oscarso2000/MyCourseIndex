import * as React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import '../style/CourseSelection.css';
import Mediacard from './MultipleCoursesModal/container';
// import { RouteComponentProps } from '@reach/router';
// import { search, handleKey, setQuery } from '../actions/index';
// import glass from '../images/glass.svg';


export interface ICSProps {
  courses?: any
}

export const CourseSelection: React.StatelessComponent<ICSProps> = ({
  courses
}: ICSProps) => {
  console.log(courses);
  //@ts-ignore
  return (
    <div className="home">
      <div className="top-bar">
        <Link to="/" target="_self" style={{ textDecoration: "none" }}>
          <h3 className="heading-1">MyCourseIndex</h3>
          <h3 className="heading-2">Search</h3>
        </Link>
        <Link to="/about" className="about-bar" style={{ textDecoration: "none" }}>
          About
        </Link>
      </div>
      <div>
        {/* 
        //@ts-ignore */}
        {courses.map((item: any, i: any) => { return <div className={"courses"} key={i}><Mediacard course={item} /> </div> })}
      </div>
    </div>
  );

}

const mapStateToProps = (state: ICSProps): ICSProps => {
  console.log(state);
  return {
    courses: state.courses
  };
};

export default connect(mapStateToProps)(CourseSelection);

