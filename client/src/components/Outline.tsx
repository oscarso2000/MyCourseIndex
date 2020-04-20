import * as React from 'react';
import { Loader } from './Loader';
import '../style/Outline.css';

interface IOutlineProp {
    outline: {
        title: string;
        text: string;
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

    if (outline.text === undefined) {
        return (
            <div className="outline">
            <h4 className="placeholder">{!!outline ? null : 'Results go here'}</h4>
            </div>
            )
    } else {
        return (
        <div className="outline">
                <h3>{!outline ? null : outline.title}</h3>
                <div dangerouslySetInnerHTML={{__html: outline.text}}></div>
        </div>
        );
    }
    
};
