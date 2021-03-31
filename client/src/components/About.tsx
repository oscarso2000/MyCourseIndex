import * as React from 'react';
import { Link } from 'react-router-dom';

import Magd from '../images/Magd_Bayoumi.png';
import Oscar from '../images/Oscar_So.jpg';
import Sheetal from '../images/Sheetal_A.jpg';
import Jenna from '../images/Jenna_Kressin.jpeg';
import Souleiman from '../images/Souleiman_B.png';
import David from '../images/David_K.png';
import Julia_N from '../images/Julia_Ng.jpg';
import Katie from '../images/Katie_Yang.jpg';
import Jessie from '../images/Jessie_Lee.png';
import John from '../images/John_O.jpg';
import Elva from '../images/Elva_Gao.jpg';
import Julia_A from '../images/Julia_A.jpg';
import Melinda from '../images/Melinda_F.jpg';
import Ruchika from '../images/Ruchika_D.png';
import Vaishnavi from '../images/Vaishnavi_G.jpeg';
import Felix from '../images/Felix_H.jpg';
import Divya from '../images/Divya_D.jpg';
import Chelsea from '../images/Chelsea_X.jpeg';
import Edward from '../images/Edward_G.jpg';
import Tobi from '../images/Tobi_A.png';
import Sam from '../images/Sam_F.jpg';


import '../style/About.css';

export const About: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link to="/">
            <h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Search</h3>
        </Link>
        <div className="center">
            <h4>About</h4>

            <p>MyCourseIndex was initially a project started for CS/INFO 4300: Language and Information that acts as an essential search engine for Cornell students and their courses. This search gathers all information from Piazza posts to Textbook and Notes Resources and returns valid results for the student to utilize. It is now being maintained and improved by members of <b><a href="https://cornelldata.science">Cornell Data Science Project Team</a></b>.</p>

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
                    <img src={Julia_N} />
                    <span className="caption"><a href="https://github.com/ngjulia">Julia Ng (jen67)</a></span>
                </div>
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
            </div>
            <p></p>
            <div className="innerimage">
                <div className="item">
                    <img src={Ruchika} />
                    <span className="caption"><a href="https://github.com/rdongre7">Ruchika Dongre (rd438)</a></span>
                </div>
                <div className="item">
                    <img src={Julia_A} />
                    <span className="caption"><a href="https://github.com/julia-allen">Julia Allen (jra264)</a></span>
                </div>
                <div className="item">
                    <img src={Melinda} />
                    <span className="caption"><a href="https://github.com/MelindaFang-code">Melinda Fang (cf348)</a></span>
                </div>
                <div className="item">
                    <img src={Divya} />
                    <span className="caption"><a href="https://github.com/Divya0204">Divya Damodaran (dd492)</a></span>
                </div>
                <div className="item">
                    <img src={Vaishnavi} />
                    <span className="caption"><a href="https://github.com/vaishnavi17">Vaishnavi Gupta (vg222)</a></span>
                </div>
            </div>
            <p></p>
            <div className="innerimage">
                <div className="item">
                    <img src={Felix} />
                    <span className="caption"><a href="https://github.com/FelixHohne">Felix Hohne (fmh42)</a></span>
                </div>
                <div className="item">
                    <img src={Tobi} />
                    <span className="caption"><a href="https://github.com/AbioticFactor">Tobi Alade (aoa34)</a></span>
                </div>
                <div className="item">
                    <img src={Chelsea} />
                    <span className="caption"><a href="https://github.com/6390wer">Chelsea Xiong (qx27)</a></span>
                </div>
                <div className="item">
                    <img src={Edward} />
                    <span className="caption"><a href="https://github.com/xegux">Edward Gu (elg227)</a></span>
                </div>
                <div className="item">
                    <img src={Sam} />
                    <span className="caption"><a href="https://github.com/samcfuchs">Sam Fuchs (scf73)</a></span>
                </div>
            </div>
            <p></p>

            <div className="centertext">
                <p> <b>Previous Members:</b> </p>
            </div>
            <div className="innerimage">
                <div className="item">
                    <img src={John} />
                    <span className="caption"><a href="https://github.com/jodonnell77">John O'Donnell (jro79)</a></span>
                </div>
            </div>
            <p></p>


            <div className="page_links" style={{display:'flex', alignItems:'center', justifyContent:'center'}}>
                <a href="Terms" target="_blank" rel="noopener noreferrer">
                    <h3 className="home-1">Terms &amp;</h3>
                    <h3 className="home-2">Conditions</h3>
                </a>

                <a href="Policy" target="_blank" rel="noopener noreferrer">
                    <h3 className="home-1">Privacy</h3>
                    <h3 className="home-2">Policy</h3>
                </a>

                <a href="https://github.com/oscarso2000/mycourseindex" target="_blank" rel="noopener noreferrer">
                    <h3 className="home-1">GitHub</h3>
                    <h3 className="home-2">Source Code</h3>
                </a>
            </div>
        </div>
    </div>
)
