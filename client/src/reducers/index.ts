import { combineReducers, applyMiddleware, createStore } from 'redux';
import thunk from 'redux-thunk';
import { counterReducer } from './counterReducer';
import { loadingStatusReducer } from './loadingStatus';
import { outlineReducer } from './outlineReducer';
import { queryReducer } from './queryReducer';
import { coursesReducer } from './coursesReducer';
import { resultsReducer } from './resultsReducer';
import { screenshotsReducer } from './screenshotsReducer';
import { orderReducer } from './orderReducer';
import { radioButtonReducer } from './radioButtonReducer';
import { foldersReducer } from './foldersReducer';
import { tagsReducer } from './tagsReducer';
import { selectedcourseReducer } from './selectedcourseReducer';
import { rvReducer } from './rvReducer';
import { formCNReducer } from './formCNReducer';
import { formPLReducer } from './formPLReducer';
import { formCLReducer } from './formCLReducer';
import { formCSVReducer } from './formCSVReducer';
import { formEmailReducer } from './formEmailReducer';
import {QAReducer} from './QAReducer';

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
    search: radioButtonReducer,
    folders: foldersReducer,
    tags: tagsReducer,
    courses: coursesReducer,
    selectedcourse: selectedcourseReducer,
    rv: rvReducer,
    formCN: formCNReducer,
    formPL: formPLReducer,
    formCL: formCLReducer,
    formCSV: formCSVReducer,
    formEmail: formEmailReducer,
    QA: QAReducer
})

const middleware = applyMiddleware(thunk)
export const store = createStore(rootReducer, middleware)
