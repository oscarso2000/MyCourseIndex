import axios from 'axios';
import { store } from '../reducers';
import { getToken } from '../config/adalConfig';


export const setQuery = (e: any): void => {
    store.dispatch({ type: 'SET_QUERY', payload: encodeURI(e.target.value) });
};

export const handleKey = (e: any, reset?: string): void => {
    if (e.key === 'Enter') {
        if (reset) {
            store.dispatch({ type: 'RESET_RESULTS' });
        }
        search();
    }
};

// TODO add token
export const search = (reset?: any): void => {
    store.dispatch<any>((dispatch: any): any => {
        if (reset) {
            dispatch({ type: 'RESET_RESULTS' });
        }
        dispatch({ type: 'LOADING_STATUS', payload: true });
        axios
            .post(`/search`, { query: store.getState().query, "token": getToken() })
            .then((res: any) => dispatch({ type: 'SEND_RESULTS', payload: res.data }))
            .then(() => {
                dispatch({ type: 'LOADING_STATUS', payload: false });
                //screenGrab();
            });
    });
};


export const setOrder = (e: any): void => {
    store.dispatch({ type: 'SET_ORDER', payload: e });
};

const screenGrab = (): void => {
    const arr = [] as any;
    const results: any = store.getState().results;
    for (let i = 0; i < results.length; i++) {
        if (!!results[i].image === false) {
            arr.push(results[i].link);
        }
    }
    getScreenshot(arr);
};

const getScreenshot = (links: string[]): void => {
    const len = links.length;
    for (let i = 0; i < len; i++) {
        const link = links[i];
        const formattedLink = encodeURIComponent(link);
        axios
            .get(`https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&url=${formattedLink}`)
            .then(res => {
                const rawData = res.data.screenshot;
                if (rawData) {
                    const imgData = rawData.data.replace(/_/g, '/').replace(/-/g, '+');
                    const screenshot = 'data:' + rawData.mime_type + ';base64,' + imgData;
                    store.dispatch({ type: 'SEND_SCREENSHOTS', payload: { link, screenshot } });
                }
            });
    }
};

export const nextPage = (): void => {
    store.dispatch<any>((dispatch: any): any => {
        dispatch({ type: 'INCREMENT' });
        // axios.post(`/results/${store.getState().query}/${store.getState().counter}`).then(res => {
        //    dispatch({ type: 'SEND_RESULTS', payload: res.data });
        //    //screenGrab();
        //});
    });
};

export const outline = (data: any): void => {
    store.dispatch<any>((dispatch: any): any => {
        dispatch({ type: 'OUTLINE_LOADING' });
        dispatch({ type: 'OUTLINE', payload: { data: data } });
    });
};
