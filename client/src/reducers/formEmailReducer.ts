import { IAction } from '.';

export const formEmailReducer = (state = '', action: IAction) => {
  switch (action.type) {
    case 'SET_FORM_EMAIL':
      return action.payload;
    default:
      return state;
  }
};