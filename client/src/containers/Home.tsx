import * as React from 'react';
import { connect } from 'react-redux';
import { SearchBox } from '../components/SearchBox';
import { ResultsView } from '../components/ResultsView';
import { search as search_fn, setQueryString, setCourseSelected } from '../actions';
import {
  useLocation,
  useHistory
} from "react-router-dom";
import qs from 'qs';

export interface IHomeProps {
    results?: any[];
    loadingStatus?: boolean;
    outline?: any;
    query: string;
    search: string;
    counter?: number;
    screenshots?: any;
    order: boolean;
    folders: string[];
    tags: string[];
    rv: boolean;
    selectedcourse?: string;
}


export const Home: React.StatelessComponent<IHomeProps> = ({
    results,
    loadingStatus,
    outline,
    query,
    search,
    screenshots,
    order,
    folders,
    tags,
    rv,
    selectedcourse,
}: IHomeProps) => {
    let location = useLocation();
    let history = useHistory();
    let course = qs.parse(location.search)["course"]
    query= qs.parse(location.search)["?query"]

    if ((course !== "" && course !== undefined && course!==selectedcourse) || selectedcourse === undefined || selectedcourse==="") {
        // console.log("No authorization! /"+location.search);
        history.push("/"+location.search);
    }
    

    if (loadingStatus === true) {
        {/* 
        // @ts-ignore */}
        return <ResultsView query={query} loadingStatus={loadingStatus} outline={outline} order={order} folders={folders} tags={tags} />;
    } else if ((loadingStatus === false && !!results && query != undefined)) {
        if (rv === true) {
            return (
                <ResultsView
                    results={results}
                    outline={outline}
                    screenshots={screenshots}
                    query={query}
                    search={search}
                    loadingStatus={loadingStatus}
                    order={order}
                    folders={folders}
                    tags={tags}
                />
            );
        } else {
            
            if (query !== undefined && !loadingStatus) {
                // console.log("search" + query);
                setQueryString(query);
                search_fn(history);
                return null;
            }

        }
    }

    return <SearchBox />;
};

const mapStateToProps = (state: IHomeProps): IHomeProps => {
    return {
        results: state.results,
        loadingStatus: state.loadingStatus,
        outline: state.outline,
        query: state.query,
        search: state.search,
        counter: state.counter,
        screenshots: state.screenshots,
        order: state.order,
        folders: state.folders,
        tags: state.tags,
        rv: state.rv,
        selectedcourse: state.selectedcourse 
    };
};

export default connect(mapStateToProps)(Home);
