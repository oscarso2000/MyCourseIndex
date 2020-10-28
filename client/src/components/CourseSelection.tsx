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
                {/* TODO1 */}
                {/* <Link to="/about" className="main-about-bar" style={{ textDecoration: "none" }}> */}
                <Link to="/form" className="main-about-bar" style={{ textDecoration: "none" }}>
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
                {/* Check to see if prof => Display "Add Course" Button that redirects to Forms Page */}
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

