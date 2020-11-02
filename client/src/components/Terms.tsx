import * as React from 'react';
import { Link } from 'react-router-dom';

import '../style/Terms.css';

export const Terms: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link to="/">
            <h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Search</h3>
        </Link>
        <div className="center">
            <h4>Terms and Conditions (TBD)</h4>
            <p></p>
            <p>1. Term 1</p>
            <p>2. Term 2</p>
            <p>3. Term 3</p>
            <p>4. Term 4</p>
            <p>5. Term 5</p>
            <p>6. Term 6</p>
            <p>7. Term 7</p>

        </div>
    </div>
)