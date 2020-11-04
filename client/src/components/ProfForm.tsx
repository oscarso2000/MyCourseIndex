import '../style/ProfForm.css';

import * as React from 'react';
import { Link } from 'react-router-dom';
import { setFormCourseName, setFormPiazzaLink, setFormCanvasLink, setFormCSVLink, setFormEmail, uploadForm } from '../actions';

export const ProfForm: React.StatelessComponent = (): JSX.Element => (
    // Code Form for Prof
    // 1. Course Name
    // 2. Piazza Link
    // 3. Piazza Token
    // 4. Student List
    <div>
        <Link to="/">
            <h3 className="home1">MyCourseIndex</h3>
            <h3 className="home2">Courses</h3>
        </Link>
        <div className="header">
            <h1 className="hl" >MyCourseIndex</h1>
        </div>
        <div className="inputForm">
            <form id="class-signup-form">
                <div className="form-field">
                    <label htmlFor="email" className="form-label">Email:</label>
                    <input type="email" className="form-input" name="email" pattern=".+@cornell.edu" title="Please use an @cornell.edu email" onChange={setFormEmail} required/>
                </div>

                <div className="form-field">
                    <label htmlFor="class-name" className="form-label">Class name:</label>
                    <input type="text" className="form-input" name="class-name" pattern="[A-Z]+ [0-9]+" title="Class Name should be formatted like this: INFO 1998" onChange={setFormCourseName} required/>
                </div>

                <div className="form-field">
                    <label htmlFor="piazza-link" className="form-label">Piazza link:</label>
                    <input type="text" className="form-input" name="piazza-link" pattern=".*piazza.com\/class\/+[A-Za-z0-9]+" onChange={setFormPiazzaLink} required/>
                </div>

                <div className="form-field">
                    <label htmlFor="canvas-link" className="form-label">Canvas Link:</label>
                    <input type="text" className="form-input" name="canvas-link" onChange={setFormCanvasLink} required/>
                </div>

                <div className="form-field">
                    <label htmlFor="csv-link" className="form-label">CSV Link:</label>
                    <input type="text" className="form-input" name="csv-link" onChange={setFormCSVLink} required/>
                </div>

                {/* <div className="form-field">
                    <label htmlFor="student-list-csv" className="form-label">Students list:</label>
                    <input type="file" className="form-input" name="student-list-csv" onChange={validateFileInput} accept=".csv" required/>
                </div> */}
                
                <input type="checkbox" name="terms-and-conds" value="2" required/>
                <label htmlFor="terms-and-conds"> I agree to the <a href="Terms" target="_blank"><u>terms &amp; conditions</u></a> and <a href="Policy" target="_blank"><u>policies</u></a> of MyCourseIndex</label>
            </form>
            <button type="submit" form="class-signup-form" onClick={uploadForm}>Submit</button>
        </div>
    </div>
);

//TODO1: Preprocess Course Name, Upload to S3 Bucket "mci-prof-form"

// Validate file input as needed. Currently does nothing
const validateFileInput = (e:any) => {
    return;
    // const file = e.target.files[0];
    // Do stuff
}