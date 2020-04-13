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
            <p> The authors of the mycourseindex project are: </p>

            <div class="item">
                <img src="../images/Magd_Bayoumi.png"/>
                <span class="caption"><a href="https://github.com/bayoumi17m">Magd Bayoumi (mb2363)</a></span>
            </div>
            <div class="item">
                <img src="../images/Jenna_Kressin.jpeg"/>
                <span class="caption"><a href="https://github.com/jek343">Jenna Kressin (jek343)</a></span>
            </div>
            <div class="item">
                <img src="../images/Souleiman_B.png"/>
                <span class="caption"><a href="https://github.com/soule">Souleiman Benhida (sb2342)</a></span>
            </div>
            <div class="item">
                <img src="../images/Sheetal_A.jpeg"/>
                <span class="caption"><a href="https://github.com/sheetal-athrey">Sheetal Athrey (spa42)</a></span>
            </div>
            <div class="item">
                <img src="../images/Oscar_So.jpg"/>
                <span class="caption"><a href="https://github.com/oscarso2000">Oscar So (ons4) </a></span>
            </div>

            <p>MyCourseIndex is...</p>  
        </div>
    </div>
)