import * as React from 'react';
import { Link } from 'react-router-dom';
import '../style/About.css';

export const About: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link to="/">
            <h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Search</h3>
        </Link>
        <div className="center">
            <h4>About</h4>
            <h4><a href="https://github.com/oscarso2000/mycourseindex">Source code on Github</a></h4>
            <p>
                The authors of the mycourseindex project are: Magd Bayoumi (mb2363), Jenna Kressin (jek343), Souleiman Benhida (sb2342), Sheetal Athrey (spa42), Oscar So (ons4) 
                MyCourseIndex is...  
            </p>  
            <ul>
                Attributions:
                <li> Icons: <a href="https://www.flaticon.com/free-icon/magnifying-glass-browser_70490#term=search&page=1&position=45">Magnifying Glass</a></li>
                    <li><a href="https://www.flaticon.com/free-icon/text-document_32329#term=text&page=1&position=9">Outline</a></li>
                    <li><a href="https://codepen.io/rbv912/pen/dYbqLQ">Loading Animation</a></li>
            </ul>
        </div>
    </div>
)