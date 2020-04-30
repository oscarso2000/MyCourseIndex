import { IAction } from '.';

const initialState = '';

export const selectedcourseReducer = (state = initialState, action: IAction) => {
  switch (action.type) {
    case 'SET_COURSE_SELECTED':
      return action;
    case 'RESET_COURSE_SELECTED':
      return initialState;
    default:
      return state;
  }
};