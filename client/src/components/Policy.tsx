import * as React from 'react';
import { Link } from 'react-router-dom';

import '../style/Policy.css';

export const Policy: React.StatelessComponent = (): JSX.Element => (
    <div>
        <Link to="/">
            <h3 className="home-1">MyCourseIndex</h3>
            <h3 className="home-2">Search</h3>
        </Link>
        <div className="center">
            <h2><strong>Policy</strong></h2>
        </div>
        
    </div>
)