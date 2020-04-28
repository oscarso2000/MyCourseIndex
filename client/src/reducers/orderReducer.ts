import { IAction } from '.';

const initialState = false;

export const orderReducer = (state = initialState, action: IAction) => {
    switch (action.type) {
        case 'SET_ORDER':
            return !state;
        default:
            return state;
    }
};