import { IAction } from '.';

export const radioButtonReducer = (state = 'Default', action: IAction) => {
    switch (action.type) {
        case 'SET_SEARCH':
          console.log(action.payload);
          return action.payload;
        default:
          return state;
      }
};