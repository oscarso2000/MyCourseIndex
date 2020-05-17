import * as React from 'react';
import { Loader } from './Loader';
import '../style/Outline.css';
import distressedEmoji from '../images/distressedEmoji.png'

interface IOutlineProp {
    outline: {
        data: any;

    };
}


export const Outline: React.StatelessComponent<IOutlineProp> = ({ outline }: IOutlineProp): JSX.Element => {
    // if (outline === 'outline loading...') {
    //     return (
    //         <div className="outline">
    //             <Loader />
    //         </div>
    //     );
    // }

    const post = [];

    if (outline.data === undefined) {
        return (
            <div className="outline">
                <h4 className="placeholder">{!!outline ? null : 'Select Result to Display Here'}</h4>
            </div>
        )
    } else if (outline.data.type === "Failure") {
        return (
            <div className="outline">
                {/* <a href={outline.data.url}><h3>{}</h3></a> */}
                <img src={distressedEmoji} style={{ height: "auto", width: "auto", verticalAlign: "middle", textAlign: "center" }}></img>
            </div>
        );
    } else if (outline.data.type === "Resource") {
        return (
            <div className="outline">
                <a target="_blank" rel="noopener noreferrer" href={outline.data.url}><h3>{"Textbook: " + outline.data.doc_name + " 🔗"}</h3></a>
                {/* <object data={outline.data.url} type="application/pdf">
                    <iframe src={"https://docs.google.com/viewer?url=" + outline.data.url + "&embedded=true"}></iframe>
                </object> */}
                {/* <div dangerouslySetInnerHTML={{ __html: outline.data.raw }}></div> */}
                <embed src={outline.data.url} key={outline.data.url} type="application/pdf" width="100%" height="600px" />
            </div>
        );
    } else { // Piazza
        const q = outline.data.raw
        post.push(<a target="_blank" rel="noopener noreferrer" href={outline.data.url}><h3>{"Piazza post: " + q.history[0].subject} 🔗</h3></a>);

        post.push(<div dangerouslySetInnerHTML={{ __html: q.history[0].content }} />);

        if (q.children) {
            q.children.forEach(function (c: any) {
                if (c.type === "i_answer") {
                    post.push(<b>Instructor Answer <small>({ "thanks! x" +c.tag_endorse_arr.length })</small></b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: c.history[0].content }} />);
                } else if (c.type === "s_answer") {
                    post.push(<b>Student Answer <small>({ "thanks! x" +c.tag_endorse_arr.length })</small> </b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: c.history[0].content }} />);
                } else { //followup
                    post.push(<b>Followup <small>({ "helpful! x" +c.tag_good_arr.length })</small></b>)
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: c.subject }} />);
                }
                c.children.forEach(function (f: any) {
                    post.push(<div className="inner"><i>Sub-followup <small>({ "helpful! x" +c.tag_good_arr.length })</small></i></div>)
                    post.push(<div className="inner" dangerouslySetInnerHTML={{ __html: f.subject }} />);
                });
            });


        }
        return (<div className="outline">{post}</div>)


    }

};
