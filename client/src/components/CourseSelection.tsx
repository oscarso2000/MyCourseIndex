import '../style/CourseSelection.css';

import * as React from 'react';

import { Link } from 'react-router-dom';
import Mediacard from './MultipleCoursesModal/container';
import Mediacardnomodal from './Mediacardnomodal';
import { connect } from 'react-redux';

// import { RouteComponentProps } from '@reach/router';
// import { search, handleKey, setQuery } from '../actions/index';
// import glass from '../images/glass.svg';


export interface ICSProps {
    courses?: any
}

export const CourseSelection: React.StatelessComponent<ICSProps> = ({
    courses
}: ICSProps) => {
    return (
        <div className="mainContainer">
            <div className="top-bar">
                {/* <Link to="/" target="_self" style={{ textDecoration: "none" }}>
          <h3 className="heading-1">MyCourseIndex</h3>
          <h3 className="heading-2">Course</h3>
        </Link> */}
                <Link to="/about" className="main-about-bar" style={{ textDecoration: "none" }}>
                    About
        </Link>
            </div>

            <div className="contentContainer">
                <div className="header">
                    <h1 className="home-logo-cs" >MyCourseIndex</h1>
                </div>
                <div className="courses">
                    {
                        courses.map((item: any, i: any) => {
                            const cardProps = {
                                course: item
                            }
                            if (item.protected) {
                                return <div className={"mediacard"} key={i}><Mediacard {...cardProps} /> </div>
                            }
                            else {
                                return <div className={"nomodalmediacard"} key={i}><Mediacardnomodal {...cardProps} /></div>
                            }
                        }
                        )
                    }
                </div>
            </div>
        </div >
    );

}

const mapStateToProps = (state: ICSProps): ICSProps => {
    return {
        courses: state.courses
    };
};

export default connect(mapStateToProps)(CourseSelection);

