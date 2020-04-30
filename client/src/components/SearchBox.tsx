import * as React from 'react';
import { Link } from 'react-router-dom';
import '../style/SearchBox.css';
import { search, handleKey, setQuery } from '../actions/index';
import glass from '../images/glass.svg';

export const SearchBox: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link className="about" to="/about">
            About
    </Link>
        <Link to="/"><h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Courses</h3></Link>

        <div className="home">
            <h1 className="home-logo">MyCourseIndex</h1> <h1 className="home-logo-2">Search</h1>
            <input onChange={e => setQuery(e)} onKeyPress={e => handleKey(e)} autoFocus={true} />
            <img onClick={search} className="glass" alt="magnifying glass" src={glass} />
        </div>
    </div >
);
