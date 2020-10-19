import { IAction } from '.';

export const formCNReducer = (state = '', action: IAction) => {
  switch (action.type) {
    case 'SET_FORM_CN':
      return action.payload;
    default:
      return state;
  }
};