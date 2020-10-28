import { IAction } from '.';

export const formPLReducer = (state = '', action: IAction) => {
  switch (action.type) {
    case 'SET_FORM_PL':
      return action.payload;
    default:
      return state;
  }
};