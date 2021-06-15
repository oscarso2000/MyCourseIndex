import * as React from 'react';
import { Loader } from './Loader';
import '../style/Outline.css';
import distressedEmoji from '../images/distressedEmoji.png'
import 'katex/dist/katex.min.css'
import Latex from 'react-latex-next'
import ReactPlayer from 'react-player/lazy'
import { object, string } from 'prop-types';


interface resComment {
    content: string;
    comments: resComment[];
    user_role?: string;
}

interface resAns {
    content: string;
    comments: resComment[];
    user_role: string;
    by?: string;
    created_at: string;
}

interface res {
    content: string;
    answers: res[];
    created_at: string;
    title: string;
}

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
    } else if (outline.data.doctype === "Failure") {
        return (
            <div className="outline">
                {/* <a href={outline.data.url}><h3>{}</h3></a> */}
                <img src={distressedEmoji} style={{ height: "auto", width: "auto", verticalAlign: "middle", textAlign: "center" }}></img>
            </div>
        );
    } else if (outline.data.doctype === "Textbook") {
        return (
            <div className="outline">
                <a target="_blank" rel="noopener noreferrer" href={outline.data.url}><h3>{"Textbook: " + outline.data.doc_name}</h3></a>
                {/* <object data={outline.data.url} type="application/pdf">
                    <iframe src={"https://docs.google.com/viewer?url=" + outline.data.url + "&embedded=true"}></iframe>
                </object> */}
                {/* <div dangerouslySetInnerHTML={{ __html: outline.data.raw }}></div> */}
                <embed src={outline.data.url} key={outline.data.url} type="application/pdf" width="100%" height="600px" />
            </div>
        );
    } else if (outline.data.doctype === "video") {
        post.push(<br></br>);
        post.push(<p>Check out the following times within the video above:</p>);
        outline.data.timestamps.forEach(function (timeHit: string) {
            post.push(<div>{timeHit}</div>);
        });
        console.log(outline.data.url);
        return (
            <div className="outline">
                <a target="_blank" rel="noopener noreferrer" href={outline.data.url}><h3>{"Video: " + outline.data.title}</h3></a>
                <ReactPlayer url={outline.data.videoUrl} controls={true} width="98%" />
                {post}
            </div>
        );
    } else if (outline.data.doctype === "EdStem") { // Piazza
        const q = outline.data;
        post.push(<a target="_blank" rel="noopener noreferrer" href={q.url}><h3>{"EdStem post: " + q.title}</h3></a>);

        post.push(<Latex>{q.content}</Latex>);
        post.push(<br></br>)
        // Loop over answers
        if (q.answers) {
            q.answers.forEach(function (ans: resAns) {
                if (ans.user_role === "admin" || ans.user_role === "staff") {
                    post.push(<b>Instructor Answer</b>);
                    post.push(<br></br>);
                    post.push(<Latex children={String(ans.content)} />);
                    // post.push(<Latex>{'$a^2 + b^2 = c^2$'}</Latex>);
                    post.push(<br></br>);
                } else if (ans.user_role === "student") {
                    post.push(<b>Student Answer</b>);
                    post.push(<br></br>);
                    post.push(<Latex children={String(ans.content)} />);
                    post.push(<br></br>);
                } else {
                    console.error(
                        "Undefined user role: Not an instructor \
                        or student ? Then what is it huh ?? "
                    );
                    post.push(<b>Student Answer</b>);
                    post.push(<br></br>);
                    post.push(<Latex children={String(ans.content)} />);
                    post.push(<br></br>);
                }
                // Comments to the answers, not to be confused with comments to the comment
                ans.comments.forEach(function (comment: any) {
                    post.push(<div className="inner"><i>Followup</i></div>);
                    post.push(<br></br>);
                    post.push(<div className="inner"><Latex children={String(comment.content)} /></div>);
                    post.push(<br></br>);
                });
            });
        };

        if (q.comments) {
            q.comments.forEach(function c(comment: any) {
                if (comment.user_role === "admin" || comment.user_role === "staff") {
                    post.push(<b>Instructor Comment</b>);
                    post.push(<Latex children={String(comment.content)} />);
                    post.push(<br></br>);
                } else if (comment.user_role === "student") {
                    post.push(<b>Student Comment</b>);
                    post.push(<Latex children={String(comment.content)} />);
                    post.push(<br></br>);
                } else {
                    console.error(
                        "Undefined user role: Not an instructor \
                        or student ? Then what is it huh ?? "
                    );
                    post.push(<b>Student Comment</b>);
                    post.push(<Latex children={String(comment.content)} />);
                    post.push(<br></br>);
                }
                // Comments to the comments - we only care about 2 levels for now
                comment.comments.forEach(function (subcomment: any) {
                    post.push(<div className="inner"><i>Sub-followup</i></div>);
                    post.push(<div className="inner"><Latex children={String(subcomment.content)} /></div>);
                    post.push(<br></br>);
                });
            });
        };

        // post.push(<div dangerouslySetInnerHTML={{ __html: q.content }} />);
        // // Loop over answers
        // if (q.answers) {
        //     q.answers.forEach(function (ans: any) {
        //         if (ans.user_role === "admin" || ans.user_role === "staff") {
        //             post.push(<b>Instructor Answer</b>);
        //             post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: ans.content }} />);
        //         } else if (ans.user_role === "student") {
        //             post.push(<b>Student Answer</b>);
        //             post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: ans.content }} />);
        //         } else {
        //             console.error(
        //                 "Undefined user role: Not an instructor \
        //                 or student ? Then what is it huh ?? "
        //             );
        //             post.push(<b>Not a student or instructor Answer</b>);
        //             post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: ans.content }} />);
        //         }
        //         // Comments to the answers, not to be confused with comments to the comment
        //         ans.comments.forEach(function (comment: any) {
        //             post.push(<div className="inner"><i>Followup</i></div>);
        //             post.push(<div className="inner" dangerouslySetInnerHTML={{ __html: comment.content }} />);
        //         });
        //     });
        // };

        // if (q.comments) {
        //     q.comments.forEach(function c(comment: any) {
        //         if (comment.user_role === "admin" || comment.user_role === "staff") {
        //             post.push(<b>Instructor Comment</b>);
        //             post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: comment.content }} />);
        //         } else if (comment.user_role === "student") {
        //             post.push(<b>Student Comment</b>);
        //             post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: comment.content }} />);
        //         } else {
        //             console.error(
        //                 "Undefined user role: Not an instructor \
        //                 or student ? Then what is it huh ?? "
        //             );
        //             post.push(<b>Not-a-student-or-instructor Comment</b>);
        //             post.push(<div style={{ textIndent: 0 }} dangerouslySetInnerHTML={{ __html: comment.content }} />);
        //         }
        //         // Comments to the comments - we only care about 2 levels for now
        //         comment.comments.forEach(function (subcomment: any) {
        //             post.push(<div className="inner"><i>Sub-followup</i></div>);
        //             post.push(<div className="inner" dangerouslySetInnerHTML={{ __html: subcomment.content }} />);
        //         });
        //     });
        // };
        return (<div className="outline">{post}</div>)
    } else {
        return (
            <div className="outline">
                {/* <a href={outline.data.url}><h3>{}</h3></a> */}
                <img src={distressedEmoji} style={{ height: "auto", width: "auto", verticalAlign: "middle", textAlign: "center" }}></img>
            </div>
        );
    }

};
