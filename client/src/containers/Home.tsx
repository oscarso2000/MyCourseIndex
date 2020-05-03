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
    order: boolean;
    folders: string[];
    tags: string[];
    rv: boolean;
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
}: IHomeProps) => {
    if (loadingStatus === true) {
        {/* 
        // @ts-ignore */}
        return <ResultsView query={query} loadingStatus={loadingStatus} outline={outline} order={order} folders={folders} tags={tags} />;
    } else if ((loadingStatus === false && !!results)) {
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
            return <SearchBox />;
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
        rv: state.rv
    };
};

export default connect(mapStateToProps)(Home);
