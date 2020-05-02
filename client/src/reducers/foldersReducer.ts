import { IAction } from '.';

export const foldersReducer = (state = [], action: IAction) => {
    switch (action.type) {
        case 'SET_FOLDERS':
          return action.payload;
        default:
          return state;
      }
};