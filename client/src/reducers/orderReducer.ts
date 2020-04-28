import { IAction } from '.';

const initialState = '';

export const orderReducer = (state = initialState, action: IAction) => {
    switch (action.type) {
        case 'SET_ORDER':
            return state === 'timestamp' ? 'timestamp' : 'score';
        default:
            return state;
    }
};