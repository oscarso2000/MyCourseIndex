import { IAction } from '.';

export const QAReducer = (state = '', action: IAction) => {
  switch (action.type) {
    case 'SET_QA':
      return action.payload;
    default:
      return state;
  }
};
