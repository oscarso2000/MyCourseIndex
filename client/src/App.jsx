import * as React from 'react';
import FadeIn from "react-fade-in";
import Lottie from "react-lottie";
import "bootstrap/dist/css/bootstrap.css";
import Home from './containers/Home';
import { About } from './components/About';
import { Switch, Route } from 'react-router-dom';
import './App.css'
import axios from "axios";
import { getToken } from './config/adalConfig';
import ReactTimeout from 'react-timeout'

import * as legoData from "./images/legoloading.json";
import * as doneData from "./images/doneloading.json";
import * as errorData from "./images/errorloading.json";


const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: legoData.default,
    rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
    }
}

const defaultOptions2 = {
    loop: false,
    autoplay: true,
    animationData: doneData.default,
    rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
    }
};

const defaultOptions3 = {
    loop: false,
    autoplay: true,
    animationData: errorData.default,
    rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
    }
};

const getAuth = (token) => {
    return axios.post(`https://www.mycourseindex.com/auth`, { "token": token }).then(
        (response) => {
            console.log(response.data);
            // console.log(typeof response.data)
            return (response.data === "OK")
        }
    )
}

const App = (props) => {

    const [authorized, setAuthorized] = React.useState(false);
    const [loaded, setLoaded] = React.useState(false);
    const [timedOut, setTimedOut] = React.useState(false);
    const [done, setDone] = React.useState(false);
    const [allowRefresh, setAllowRefresh] = React.useState(false)

    React.useEffect(() => {
        // TODO: Figure out how to remove autoRefresh on close
        // window.addEventListener('unload', function (event) {
        //     sessionStorage.removeItem("allowRefresh");
        // });
        setAllowRefresh(sessionStorage.getItem("allowRefresh") === "True");
        console.log(allowRefresh);
        if (allowRefresh) {
            const auth = getAuth(getToken());
            auth.then((value) => {
                setAuthorized(value);
                setLoaded(true);
                setDone(true);
                setTimedOut(true);
            });
        } else {
            props.setTimeout(() => {
                const auth = getAuth(getToken());
                auth.then((value) => {
                    setAuthorized(value);
                    setLoaded(true);
                    setDone(true);
                    props.setTimeout(() => {
                        setTimedOut(true);
                        sessionStorage.setItem("allowRefresh", "True")
                    }, 1000)
                });
            }, 3000);
        }
    });

    console.log('done is ' + done + '\nloaded is ' + loaded + '\ntimedOut is ' + timedOut + '\nauthorized is ' + authorized);

    if (loaded && done && timedOut) {
        if (authorized) {
            return (
                <div>
                    <Switch>
                        <Route exact={true} path="/" component={Home} />
                        <Route path="/about" component={About} />
                    </Switch>
                </div>
            )
        } else {
            return (
                <div className="App">
                    <header className="App-header">
                        <FadeIn>
                            <div class="d-flex justify-content-center align-items-center">
                                <h1 style={{ color: "#FFFFFF" }}>Not Authorized!</h1>
                            </div>
                        </FadeIn>
                    </header >
                </div >
            )
        }
    } else if (allowRefresh) {
        return (<div></div>)
    } else {
        return (
            <div className="App">
                <header className="App-header">
                    <FadeIn>
                        <div class="d-flex justify-content-center align-items-center">
                            <h1>Fetching Authorization</h1>
                            {done ?
                                (authorized ?
                                    <Lottie options={defaultOptions2} height={480} width={480} /> :
                                    <Lottie options={defaultOptions3} height={480} width={480} />
                                )
                                : (<Lottie options={defaultOptions} height={480} width={480} />
                                )}
                        </div>
                    </FadeIn>
                </header >
            </div >
        )
    }
}

export const Application = ReactTimeout(App);
