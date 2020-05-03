import { IAction } from '.';

export const tagsReducer = (state = [], action: IAction) => {
    switch (action.type) {
        case 'SET_TAGS':
          return action.payload;
        default:
          return state;
      }
};