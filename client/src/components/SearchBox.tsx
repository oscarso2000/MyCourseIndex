import '../style/SearchBox.css';

import * as React from 'react';

import { handleKey, search, setQuery } from '../actions/index';
import {
  useHistory,
  useLocation
} from "react-router-dom";

import { Link } from 'react-router-dom';
import glass from '../images/glass.svg';
import qs from 'qs';

export const SearchBox: React.StatelessComponent = (): JSX.Element => {
    let history = useHistory();

    return (
    <div>
        <Link className="about" to="/about">
            About
        </Link>
        <Link to="/">
            <h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Courses</h3>
        </Link>

        <div className="main">
            <div className="home">
                <div className="home-logo-header">
                    <h1 className="home-logo">MyCourseIndex</h1>
                    <h1 className="home-logo-2">Search</h1>
                </div>
                <div className="home-search-section">
                    <div className="home-search-bar">
                        <input onChange={e => setQuery(e)} onKeyPress={e => handleKey(e,history)} autoFocus={true} />
                        <img onClick={() => search(history)} className="glass" alt="magnifying glass" src={glass} />
                    </div>
                    <div className="help-tip">
                        <p><b>For Advanced Searches:</b><br />1) +’query’ for mandatory inclusion.<br />2) -’query’ for mandatory exclusion.<br />3) ‘query^n to emphasize n times. </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
);
}
