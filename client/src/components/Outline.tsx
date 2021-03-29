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
        const q = outline.data;
        post.push(<a target="_blank" rel="noopener noreferrer" href={q.url}><h3>{"Piazza post: " + q.title} 🔗</h3></a>);

        post.push(<div dangerouslySetInnerHTML={{ __html: q.history[0].content }} />);
        // Loop over answers
        if (q.answers) {
            q.answers.forEach(function (ans: any) {
                if (ans.user_role === "admin" || ans.user_role === "staff") {
                    post.push(<b>Instructor Answer</b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: ans.content }} />);
                } else if (ans.user_role === "student") {
                    post.push(<b>Student Answer</b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: ans.content }} />);
                } else {
                    console.error(
                        "Undefined user role: Not an instructor \
                        or student ? Then what is it huh ?? "
                    );
                    post.push(<b>Not a student or instructor Answer</b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: ans.content }} />);
                }
                // Comments to the answers, not to be confused with comments to the comment
                ans.comments.forEach(function (comment: any) {
                    post.push(<div className="inner"><i>Followup</i></div>);
                    post.push(<div className="inner" dangerouslySetInnerHTML={{ __html: comment.content }} />);
                });
            });
        };

        if (q.comments) {
            q.comments.forEach(function c(comment: any) {
                if (comment.user_role === "admin" || comment.user_role === "staff") {
                    post.push(<b>Instructor Comment</b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: comment.content }} />);
                } else if (comment.user_role === "student") {
                    post.push(<b>Student Comment</b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: comment.content }} />);
                } else {
                    console.error(
                        "Undefined user role: Not an instructor \
                        or student ? Then what is it huh ?? "
                    );
                    post.push(<b>Not-a-student-or-instructor Comment</b>);
                    post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: comment.content }} />);
                }
                // Comments to the comments - we only care about 2 levels for now
                comment.comments.forEach(function (subcomment: any) {
                    post.push(<div className="inner"><i>Sub-followup</i></div>);
                    post.push(<div className="inner" dangerouslySetInnerHTML={{ __html: subcomment.content }} />);
                });
            });
        };
        return (<div className="outline">{post}</div>)


    }

};
