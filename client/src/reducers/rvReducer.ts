import { IAction } from '.';

export const rvReducer = (state = false, action: IAction) => {
  switch (action.type) {
    case 'RV_STATUS':
      return action.payload;
    default:
      return state;
  }
};
