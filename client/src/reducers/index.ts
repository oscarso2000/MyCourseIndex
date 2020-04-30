import { combineReducers, applyMiddleware, createStore } from 'redux';
import thunk from 'redux-thunk';
import { counterReducer } from './counterReducer';
import { loadingStatusReducer } from './loadingStatus';
import { outlineReducer } from './outlineReducer';
import { queryReducer } from './queryReducer';
import { coursesReducer } from './coursesReducer';
import { resultsReducer } from './resultsReducer';
import { screenshotsReducer } from './screenshotsReducer';
import { selectedcourseReducer } from './selectedcourseReducer';

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
  courses: coursesReducer,
  screenshots: screenshotsReducer,
  selectedcourse: selectedcourseReducer
})

const middleware = applyMiddleware(thunk)
export const store = createStore(rootReducer, middleware)
