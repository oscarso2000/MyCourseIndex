import React from 'react';
import { Link } from 'react-router-dom';
export const Form = ({ onSubmit }) => {
  return (
    <form onSubmit={onSubmit} >
      <div className="form-group">
        <label htmlFor="Token">Token</label>
        <input className="form-control" id="Token" />
      </div>

      {/* <div className="form-group">
        <label htmlFor="email">Email address</label>
        <input type="email" className="form-control" id="email"
          placeholder="name@example.com"
        />
      </div> */}
      <div className="form-group">
        <button className="form-control btn btn-primary" type="submit">
          Submit
        </button>
      </div>
    </form>
  );
};
export default Form;