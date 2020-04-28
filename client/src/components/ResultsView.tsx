import * as React from 'react';
import { ResultsList } from './ResultsList';
import { Link } from 'react-router-dom';
import { Outline } from './Outline';
import { handleKey, search, setQuery, setOrder } from '../actions';
import '../style/ResultsView.css';
import glass from '../images/glass.svg';
import { Loader } from './Loader';

export const ResultsView: React.StatelessComponent<any> = ({ results, outline, screenshots, query, loadingStatus, order }: any): JSX.Element => {
    const mobile: string[] = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry'];
    const ASC = 'ascending';
    const DSC = 'descending';

    const sortByTimestamp = (a: any, b: any, sortOrder: any = DSC) => {
        const diff = a.timestamp.toLowerCase().localeCompare(b.text.toLowerCase());

        if (sortOrder === ASC) {
            return diff;
        }
        return -1 * diff;
    }


    const sortByScore = (a: any, b: any, sortOrder: any = DSC) => {
        const diff = a.score - b.score;

        if (sortOrder === ASC) {
            return diff;
        }
        return -1 * diff;
    }

    if (results && results.length > 0) {
        if (order === 'timestamp') {
            results.sort((a: any, b: any) => sortByTimestamp(a, b));
        } else {
            results.sort((a: any, b: any) => sortByScore(a, b));
        }
    }

    return (
        <div>
            <div className="top-bar">
                <Link to="/" target="_self" style={{ textDecoration: "none" }}>
                    <h3 className="heading-1">MyCourseIndex</h3>
                    <h3 className="heading-2">Search</h3>
                </Link>
                <input
                    defaultValue={decodeURI(query)}
                    onKeyPress={e => handleKey(e, 'reset')}
                    onChange={e => setQuery(e)}
                />
                <img onClick={() => search('reset')} className="glass" alt="magnifying glass" src={glass} />
                <div className="radioButtons">
                    <label className="searchSel" onChange={e => setOrder(e)}>Sort by Time
                    <input type="radio" value="timestamp" name="s" />
                        <span className="checkmark"></span>
                    </label>
                </div>
                <Link to="/about" className="about-bar" style={{ textDecoration: "none" }}>
                    About
                </Link>
            </div>
            <Outline outline={outline} />
            {loadingStatus === true
                ? <div className={mobile.includes(navigator.platform) ? "" : "load-wrap"}><Loader /></div>
                : <ResultsList results={results} screenshots={screenshots} />
            }
        </div>
    );
};
