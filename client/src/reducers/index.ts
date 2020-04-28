import { combineReducers, applyMiddleware, createStore } from 'redux';
import thunk from 'redux-thunk';
import { counterReducer } from './counterReducer';
import { loadingStatusReducer } from './loadingStatus';
import { outlineReducer } from './outlineReducer';
import { queryReducer } from './queryReducer';
import { resultsReducer } from './resultsReducer';
import { screenshotsReducer } from './screenshotsReducer';
import { orderReducer } from './orderReducer';
import { radioButtonReducer } from './radioButtonReducer';

export interface IAction {
    type: string;
    payload?: any;
}

export const rootReducer = combineReducers({
    results: resultsReducer,
    loadingStatus: loadingStatusReducer,
    outline: outlineReducer,
    query: queryReducer,
    counter: counterReducer,
    screenshots: screenshotsReducer,
    order: orderReducer,
    search: radioButtonReducer
})

const middleware = applyMiddleware(thunk)
export const store = createStore(rootReducer, middleware)
