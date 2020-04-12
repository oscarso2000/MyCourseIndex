import * as React from 'react';
import { WindMillLoading } from 'react-loadingg';
import Home from './containers/Home';
import { About } from './components/About';
import { Switch, Route } from 'react-router-dom';
import './App.css'
import axios from "axios";
import { getToken } from './config/adalConfig';

// export const App: React.StatelessComponent = (): JSX.Element => {
//     return (
//         <div>
//             <Switch>
//                 <Route exact={true} path="/" component={Home} />
//                 <Route path="/about" component={About} />
//             </Switch>
//         </div>
//     )
// }

const getAuth = (token) => {
    return axios.post(`https://www.mycourseindex.com/auth`, { "token": token }).then(
        (response) => {
            // console.log(response.data);
            // console.log(typeof response.data)
            return (response.data === "OK")
        }
    )
}

const divLoadingStyle = {
    textAlign: 'center',
    verticalAlign: 'middle'
}

const windmillStyle = {
    display: 'inline-block'
}

export const App = () => {

    const [authorized, setAuthorized] = React.useState(false);
    const [loaded, setLoaded] = React.useState(false);

    const auth = getAuth(getToken());
    auth.then((value) => {
        setAuthorized(value);
        setLoaded(true);
    });

    console.log("Auth");
    console.log(auth);
    if (loaded) {
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
                <div>
                    <p>
                        ERROR!
                    </p>
                </div>
            )
        }
    } else {
        return (
            <div style={divLoadingStyle}>
                <WindMillLoading color="#00CDCD" size="large" style={windmillStyle} />
                Loading...
            </div>
        )
    }
}

// export const App = () => {
//     if (true) {
//         return (
//             <div >
//                 <Switch>
//                     <Route exact={true} path="/" component={Home} />
//                     <Route path="/about" component={About} />
//                 </Switch>
//             </div >
//         );
//     }
//     return (
//         <div>
//             <p>
//                 Error
//             </p>
//         </div>
//     );
// }
