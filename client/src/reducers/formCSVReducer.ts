import { IAction } from '.';

export const formCSVReducer = (state = '', action: IAction) => {
  switch (action.type) {
    case 'SET_FORM_CSV':
      return action.payload;
    default:
      return state;
  }
};