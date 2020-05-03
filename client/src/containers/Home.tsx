import * as React from 'react';
import { connect } from 'react-redux';
import { SearchBox } from '../components/SearchBox';
import { ResultsView } from '../components/ResultsView';

export interface IHomeProps {
    results?: any[];
    loadingStatus?: boolean;
    outline?: any;
    query: string;
    filter: string;
    counter?: number;
    screenshots?: any;
    order: boolean
    folders: string[];
    tags: string[];
}

export const Home: React.StatelessComponent<IHomeProps> = ({
    results,
    loadingStatus,
    outline,
    query,
    filter,
    screenshots,
    order,
    folders,
    tags,
}: IHomeProps) => {
    if (loadingStatus === true) {
        {/* 
        // @ts-ignore */}
        return <ResultsView query={query} loadingStatus={loadingStatus} outline={outline} order={order} folders={folders} tags={tags} />;
    } else if (loadingStatus === false && !!results) {
        return (
            <ResultsView
                results={results}
                outline={outline}
                screenshots={screenshots}
                query={query}
                filter={filter}
                loadingStatus={loadingStatus}
                order={order}
                folders={folders}
                tags={tags}
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
        filter: state.filter,
        counter: state.counter,
        screenshots: state.screenshots,
        order: state.order,
        folders: state.folders,
        tags: state.tags
    };
};

export default connect(mapStateToProps)(Home);
