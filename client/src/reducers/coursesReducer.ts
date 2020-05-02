import { IAction } from '.';

const initialState = '';

export const coursesReducer = (state = initialState, action: IAction) => {
  switch (action.type) {
    case 'SET_COURSES':
      return action.payload;
    case 'RESET_COURSES':
      return initialState;
    default:
      return state;
  }
};