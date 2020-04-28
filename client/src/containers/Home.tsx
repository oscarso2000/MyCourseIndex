import * as React from 'react';
import { connect } from 'react-redux';
import { SearchBox } from '../components/SearchBox';
import { ResultsView } from '../components/ResultsView';

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
    if (loadingStatus === true) {
        {/* 
        // @ts-ignore */}
        return <ResultsView query={query} loadingStatus={loadingStatus} outline={outline} order={order} />;
    } else if (loadingStatus === false && !!results) {
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
        order: state.order
    };
};

export default connect(mapStateToProps)(Home);
