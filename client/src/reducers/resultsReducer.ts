import { IAction } from '.';

const initialState: [] = [];

export const resultsReducer = (state = initialState, action: IAction) => {
    switch (action.type) {
        case 'SEND_RESULTS':
            // console.log(action.payload);
            return !!state === true ? initialState.concat(action.payload) : action.payload;
        case 'RESET_RESULTS':
            return initialState;
        default:
            return state;
    }
};
