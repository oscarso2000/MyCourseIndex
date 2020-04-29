import * as React from 'react';
import { Link } from 'react-router-dom';
import '../style/SearchBox.css';
import { search, handleKey, setQuery, setSearchSel } from '../actions/index';
import glass from '../images/glass.svg';

export const SearchBox: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link className="about" to="/about">
            About
        </Link>
        <div className = "main">
            <div className="home">
                <h1 className="home-logo">MyCourseIndex</h1> <h1 className="home-logo-2">Search</h1>
                <input onChange={e => setQuery(e)} onKeyPress={e => handleKey(e)} autoFocus={true} />
                <img onClick={search} className="glass" alt="magnifying glass" src={glass} />
                <div className="help-tip">
                    <p><b>For Advanced Searches:</b><br/>1) +’query’ for mandatory inclusion.<br/>2) -’query’ for mandatory exclusion.<br/>3) ‘query^n to emphasize n times. </p>
                    {/* <p>Use +'word/phrase' for mandatory results. 2) Use -'word/phrase' to remove from results. 3) Use 'word'^n to emphasize the particular word n times.</p> */}
                </div>
            </div>
            <div className ="radioButtons">
                <label className="searchSel" onChange = {e => setSearchSel(e)}>Search Everything
                    <input type="radio" value="Default" name = "s" defaultChecked/>
                    <span className="checkmark"></span>
                </label>
                <label className="searchSel" onChange = {e => setSearchSel(e)}>Search Piazza Only
                    <input type="radio" value="Piazza" name = "s" />
                    <span className="checkmark"></span>
                </label>
                <label className="searchSel" onChange = {e => setSearchSel(e)}>Search Resources Only
                    <input type="radio" value="Resource" name = "s" />
                    <span className="checkmark"></span>
                </label>
                {/* <input type="radio" value="Default" name="searchSel" defaultChecked/> Search Everything
                <input type="radio" value="Piazza" name="searchSel" /> Search Piazza Only
                <input type="radio" value="Resource" name="searchSel" /> Search Resources Only */}
            </div>
        </div>
    </div>
);
