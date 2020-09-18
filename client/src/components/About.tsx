import * as React from 'react';
import { Link } from 'react-router-dom';

import Magd from '../images/Magd_Bayoumi.png';
import Oscar from '../images/Oscar_So.jpg';
import Sheetal from '../images/Sheetal_A.jpg';
import Jenna from '../images/Jenna_Kressin.jpeg';
import Souleiman from '../images/Souleiman_B.png';
import David from '../images/David_Kim.jpg';
import Julia from '../images/Julia_Ng.jpg';
import Katie from '../images/Katie_Yang.jpg';
import Jessie from '../images/Jessie_Lee.png';
import John from '../images/John_O.jpg'
import Elva from '../images/Elva_Gao.jpg'

import '../style/About.css';

export const About: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link to="/">
            <h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Search</h3>
        </Link>
        <div className="centerAbout">
            <h4>About</h4>

            <p>MyCourseIndex was initially a project started for CS/INFO 4300: Language and Information that acts as an essential search engine for Cornell students and their courses. This search gathers all information from Piazza posts to Textbook and Notes Resources and returns valid results for the student to utilize. It is now being maintained and improved by members of <a href="https://cornelldata.science">Cornell Data Science Project Team</a>.</p>

            <div className="centertext">
                <p> <b>Co-Founders:</b> </p>
            </div>
            <div className="innerimage">
                <div className="item">
                    <img src={Magd} />
                    <span className="caption"><a href="https://github.com/bayoumi17m">Magd Bayoumi (mb2363)</a></span>
                </div>
                <div className="item">
                    <img src={Jenna} />
                    <span className="caption"><a href="https://github.com/jek343">Jenna Kressin (jek343)</a></span>
                </div>
                <div className="item">
                    <img src={Souleiman} />
                    <span className="caption"><a href="https://github.com/soule">Souleiman Benhida (sb2342)</a></span>
                </div>
                <div className="item">
                    <img src={Sheetal} />
                    <span className="caption"><a href="https://github.com/sheetal-athrey">Sheetal Athrey (spa42)</a></span>
                </div>
                <div className="item">
                    <img src={Oscar} />
                    <span className="caption"><a href="https://github.com/oscarso2000">Oscar So (ons4)</a></span>
                </div>
            </div>
            <p></p>

            <div className="centertext">
                <p> <b>Team:</b> </p>
            </div>

            <div className="innerimage">
                <div className="item">
                    <img src={David} />
                    <span className="caption"><a href="https://github.com/TrueshotBarrage">David Kim (jk2537)</a></span>
                </div>
                <div className="item">
                    <img src={Jessie} />
                    <span className="caption"><a href="https://github.com/shljessie">Jessie Lee (sl994)</a></span>
                </div>
                <div className="item">
                    <img src={Julia} />
                    <span className="caption"><a href="https://github.com/ngjulia">Julia Ng (jen67)</a></span>
                </div>
            </div>
            <p></p>
            <div className="innerimage">
                <div className="item">
                    <img src={Katie} />
                    <span className="caption"><a href="https://github.com/yangkt">Katie Yang (ky289)</a></span>
                </div>
                <div className="item">
                    <img src={Elva} />
                    {/* Personal GitHub */}
                    {/* <span className="caption"><a href="https://github.com/elvagao66">Elva Gao (yg357)</a></span> */}
                    <span className="caption"><a href="https://github.com/elvaaaa">Elva Gao (yg357)</a></span>
                </div>
                <div className="item">
                    <img src={John} />
                    <span className="caption"><a href="https://github.com/jodonnell77">John O'Donnell (jro79)</a></span>
                </div>
            </div>

            <p></p>

            <a href="https://v1.mycourseindex.com" target="_blank">
                <h3 className="home-1">MyCourseIndex</h3>
                <h3 className="home-2">Search V1</h3>
            </a>

            <a href="https://v2.mycourseindex.com" target="_blank">
                <h3 className="home-1">MyCourseIndex</h3>
                <h3 className="home-2">Search V2</h3>
            </a>

            <a href="https://github.com/oscarso2000/mycourseindex" target="_blank">
                <h3 className="home-1">GitHub</h3>
                <h3 className="home-2">Source Code</h3>
            </a>

            {/* Adding space to bottom of page */}
            <p></p>
            <p></p>

        </div>
    </div>
)