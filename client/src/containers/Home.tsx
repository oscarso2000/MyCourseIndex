import * as React from 'react';
import { connect } from 'react-redux';
import { SearchBox } from '../components/SearchBox';
import { ResultsView } from '../components/ResultsView';
import { handleKey, search1, setQuery, setQueryString, setOrder, setSearchSel } from '../actions';
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
    order: boolean
}

export const Home: React.StatelessComponent<IHomeProps> = ({
    results,
    loadingStatus,
    outline,
    query,
    search,
    screenshots,
    order,
}: IHomeProps) => {

    let location = useLocation();
    let history = useHistory();
    query= qs.parse(location.search)["?query"]
        

    if (loadingStatus === true) {
        {/* 
        // @ts-ignore */}
        return <ResultsView query={query} loadingStatus={loadingStatus} outline={outline} order={order} />;

    } else if (loadingStatus === false && !!results && query != undefined) {
        return (
            <ResultsView
                results={results}
                outline={outline}
                screenshots={screenshots}
                query={query}
                search={search}
                loadingStatus={loadingStatus}
                order={order}
            />
        );
    }
    
    if (query===undefined) {
        return <SearchBox />;
    } else {
        setQueryString(query);
        search1();
        return null;
    }

    
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
        order: state.order
    };
};

export default connect(mapStateToProps)(Home);
