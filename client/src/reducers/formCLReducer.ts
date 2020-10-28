import { IAction } from '.';

export const formCLReducer = (state = '', action: IAction) => {
  switch (action.type) {
    case 'SET_FORM_CL':
      return action.payload;
    default:
      return state;
  }
};