import axios from "axios";
import { store } from "../reducers";
import { getToken } from "../config/adalConfig";

export const setQuery = (e: any): void => {
    store.dispatch({ type: "SET_QUERY", payload: encodeURI(e.target.value) });
};

export const setQueryString = (e: any): void => {
    store.dispatch({ type: 'SET_QUERY', payload: encodeURI(e) });
};

export const setSearchSel = (e: any): void => {
    store.dispatch({ type: "SET_SEARCH", payload: encodeURI(e.target.value) });
};

export const setTags = (e: any, value: string[]): void => {
    store.dispatch({ type: 'SET_TAGS', payload: value });
};

export const setCourses = (e: any): void => {
    store.dispatch({ type: 'SET_COURSES', payload: e });
}

export const setCourseSelected = (e: any): any => {
    store.dispatch({
        type: 'SET_COURSE_SELECTED', payload: e
    });
}

export const handleKey = (e: any, history: any, reset?: string): void => {
    if (e.key === "Enter") {
        // if (reset) {
        //   store.dispatch({ type: "RESET_RESULTS" });
        // }
        search(history);
    }
};
export const handleKey1 = (e: any, history: any, reset?: string): void => {
    if (e.key === "Enter") {
        // if (reset) {
        //   store.dispatch({ type: "RESET_RESULTS" });
        // }
        search1(history);
    }
};

// TODO add token
export const search = (history: any, reset?: any): void => {
    store.dispatch<any>((dispatch: any): any => {
        // if (reset) {
        //   dispatch({ type: "RESET_RESULTS" });
        // }
        axios
            .post(`/folders`, { courseSelection: store.getState().selectedcourse })
            .then((res: any) => dispatch({ type: "SET_FOLDERS", payload: res.data }))
            .then(() => {
                dispatch({ type: "LOADING_STATUS", payload: true });
                dispatch({ type: "RV_STATUS", payload: true });
                dispatch({ type: "OUTLINE", payload: '' });
            });
        axios
            .post(`/search`, {
                query: store.getState().query,
                token: getToken(),
                search: store.getState().search,
                course: store.getState().selectedcourse,
            })
            .then((res: any) => dispatch({ type: "SEND_RESULTS", payload: res.data }))
            .then(() => {
                dispatch({ type: "LOADING_STATUS", payload: false });
                history.push("/browse?query="+store.getState().query+"&course="+store.getState().selectedcourse);
                //screenGrab();
            });
    });
};
export const search1 = (history: any, reset?: any): void => {
    store.dispatch<any>((dispatch: any): any => {
        // if (reset) {
        //   dispatch({ type: "RESET_RESULTS" });
        // }
        dispatch({ type: "LOADING_STATUS", payload: true });
        dispatch({ type: "RV_STATUS", payload: true });
        dispatch({ type: "OUTLINE", payload: '' });
        axios
            .post(`/search`, {
                query: store.getState().query,
                token: getToken(),
                search: store.getState().search,
                course: store.getState().selectedcourse,
            })
            .then((res: any) => dispatch({ type: "SEND_RESULTS", payload: res.data }))
            .then(() => {
                dispatch({ type: "LOADING_STATUS", payload: false });
                history.push("/browse?query="+store.getState().query+"&course="+store.getState().selectedcourse);
                //screenGrab();
            });
    });
};

export const setOrder = (e: any): void => {
    // console.log(e);
    store.dispatch({ type: "SET_ORDER", payload: e });
};

export const accessProtectedCourse: (token: string | null) => Promise<boolean> = async (token) => {
    const response = await axios.post(`/tokeVerify`, { "token": getToken(), course: store.getState().selectedcourse, piazzaToken: token });
    return (response.data === "OK");
}

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
            .get(
                `https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&url=${formattedLink}`
            )
            .then((res) => {
                const rawData = res.data.screenshot;
                if (rawData) {
                    const imgData = rawData.data.replace(/_/g, "/").replace(/-/g, "+");
                    const screenshot = "data:" + rawData.mime_type + ";base64," + imgData;
                    store.dispatch({
                        type: "SEND_SCREENSHOTS",
                        payload: { link, screenshot },
                    });
                }
            });
    }
};

export const nextPage = (): void => {
    store.dispatch<any>((dispatch: any): any => {
        dispatch({ type: "INCREMENT" });
        // axios.post(`/results/${store.getState().query}/${store.getState().counter}`).then(res => {
        //    dispatch({ type: 'SEND_RESULTS', payload: res.data });
        //    //screenGrab();
        //});
    });
};

// export const getConfirmation = (): void => {
//     store.dispatch<any>((dispatch: any): any => {
//         dispatch({ type: 'GET_CONFIRMATION' });
//     });
// };

export const outline = (data: any): void => {
    store.dispatch<any>((dispatch: any): any => {
        dispatch({ type: "OUTLINE_LOADING" });
        dispatch({ type: "OUTLINE", payload: { data: data } });
    });
};
