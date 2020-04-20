import * as React from 'react';
import Tooltip from 'rc-tooltip';
import 'rc-tooltip/assets/bootstrap_white.css';
import '../style/Result.css';
import { outline } from '../actions';
import imgLoader from '../images/imgLoader.gif';
import document from '../images/document.svg';

export interface IData {
    title: string;
    link: string;
    snippet?: string;
    favicon?: string;
    pagemap?: { cse_image?: any };
}

interface IResultProps {
    data: Record<string, any>;
    screenshots: string[];
}

const resolveImage = (pagemap: IData['pagemap'], link: string, screenshots: any[]) => {
    if (pagemap && pagemap.cse_image) {
        const [{ src }] = pagemap.cse_image;
        return src;
    } else {
        for (let i = 0; i < screenshots.length; i++) {
            if (screenshots[i].link === link) {
                return screenshots[i].screenshot;
            }
        }
        return imgLoader;
    }
};
export const Result = ({data,screenshots}: IResultProps) => (
    <div className="card">
        <div className="card-body">
            <h4 className="title" onClick={() => outline(data)}>{data.history[0].subject} </h4>
            <div className="wrap">
                <p className="description" dangerouslySetInnerHTML={{__html: data.history[0].content}} ></p>
            </div>
        </div>
    </div>

);
export const Result2 = ({ data, screenshots }: IResultProps) => (
    <div className="card">
        <a target="_blank" rel="noopener noreferrer" >
            <img className="preview" alt="I is here" src={resolveImage(data.pagemap, data.link, screenshots)} />
        </a>
        <div className="card-body">
            <a target="_blank" rel="noopener noreferrer">
                <img
                    className="favicon"
                    alt="I is here"
                    src={`https://www.google.com/s2/favicons?domain=${data.link}`}
                />
            </a>
            <h4 className="title">
                <a className="ext-link" target="_blank" rel="noopener noreferrer" href={decodeURI(data.link)}>
                    
                </a>
            </h4>
            <Tooltip
                placement="right"
                overlay={'Text-Only Outline'}
                arrowContent={<div className="rc-tooltip-arrow-inner" />}
            >
                <img className="icon" alt="outline" src={document} onClick={() => outline(data.link)} />
            </Tooltip>
            <div className="wrap">
                <p className="description">{data.snippet}</p>
            </div>
        </div>
    </div>
);
