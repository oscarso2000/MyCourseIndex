import * as React from 'react';
import { ResultsList } from './ResultsList';
import { Link } from 'react-router-dom';
import { Outline } from './Outline';
import { handleKey, search, setQuery, setOrder } from '../actions';
import '../style/ResultsView.css';
import glass from '../images/glass.svg';
import { Loader } from './Loader';
import Switch from '@material-ui/core/Switch';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';

export const ResultsView: React.StatelessComponent<any> = ({ results, outline, screenshots, query, loadingStatus, order }: any): JSX.Element => {
    const mobile: string[] = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry'];
    const ASC = 'ascending';
    const DSC = 'descending';

    const sortByTimestamp = (a: any, b: any, sortOrder: any = DSC) => {
        // console.log(a);
        const diff = a.timestamp.toLowerCase().localeCompare(b.timestamp.toLowerCase());

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

    // const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    //     // event.persist();
    //     // console.log(event.target.checked);
    //     console.log("Clicked");
    //     setOrder(!order);
    // };

    const handleChange = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        // event.persist();
        // console.log(event.target.checked);
        // console.log("Clicked");
        setOrder(!order);
    };

    if (results && results.length > 0) {
        if (order) {
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
                <Switch
                    checked={order}
                    onClick={handleChange}
                    name="checkedB"
                    color="primary"
                />
                <h3 className="heading-2">Sort by most recent</h3>

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
