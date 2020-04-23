import * as React from 'react';
import * as InfiniteScroll from 'react-infinite-scroll-component';
import { nextPage } from '../actions/index';
import { Result } from './Result';
import { outline } from '../actions';
// import { IData } from './Result';

// interface IResultsListProps {
//     results: any[];
//     screenshots: string[];
// }



export const ResultsList = ({ results, screenshots }) => {
    const ResultsArray = [];
    const len = results.length;

    for (let i = 0; i < len; i++) {
        // console.log(results[i])
        ResultsArray.push(<Result data={results[i]} screenshots={screenshots} />);
    }

    if (ResultsArray.length === 0) {
        return (
            <div className="card" onClick={() => outline({ type: "Failure" })}>
                <div className="card-body">
                    <h4 className="title" >No Results Found... 😢 Sorry.</h4>
                    <div className="">
                        <p className="description" dangerouslySetInnerHTML={{ __html: "Try maybe asking on Piazza!" }} ></p>
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <InfiniteScroll
                dataLength={len}
                next={nextPage}
                hasMore={false}
                loader={<p className="loading-text">Loading...</p>}
            >
                {ResultsArray}
            </InfiniteScroll>
        );
    }
};


// export const ResultsList = ({ results, screenshots }: IResultsListProps): JSX.Element => {
//     const ResultsArray = [] as any;
//     const len = results.length;

//     for (let i = 0; i < len; i++) {
//         ResultsArray.push(<Result data={results[i] as IData} screenshots={screenshots} />);
//     }

//     return (
//         <InfiniteScroll
//             dataLength={len}
//             next={nextPage}
//             hasMore={true}
//             loader={<p className="loading-text">Loading...</p>}
//         >
//             {ResultsArray}
//         </InfiniteScroll>
//     );
// };