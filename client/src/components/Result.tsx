import * as React from 'react';
import Tooltip from 'rc-tooltip';
import 'rc-tooltip/assets/bootstrap_white.css';
import '../style/Result.css';
import { outline } from '../actions';
import imgLoader from '../images/imgLoader.gif';
import document from '../images/document.svg';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import Chip from '@material-ui/core/Chip';
import Paper from '@material-ui/core/Paper';
// import TagFacesIcon from '@material-ui/icons/TagFaces';
// import ComputerTwoToneIcon from '@material-ui/icons/ComputerTwoTone';
import FaceIcon from '@material-ui/icons/Face';
import { any } from 'prop-types';

interface ChipData {
    key: number;
    label: string;
}

const useStyles = makeStyles((theme: Theme) =>
    createStyles({
        root: {
            display: 'flex',
            backgroundColor: 'transparent',
            // justifyContent: 'center',
            float: 'right',
            flexWrap: 'wrap',
            listStyle: 'none',
            padding: theme.spacing(0.1),
            margin: 0,
        },
        chip: {
            margin: theme.spacing(0.5),
        },
    }),
);

const ChipsArray: React.FC<string[]> = (concepts: string[]) => {
    const classes = useStyles();

    return (
        <Paper component="ul" className={classes.root} elevation={0}>
            {Object.keys(concepts).map((key: any, index: any) => {
                let icon;
                if (true) {
                    icon = FaceIcon;
                }

                return (
                    <li key={String(index) + concepts[key]}>
                        <Chip
                            label={concepts[key]}
                            onDelete={undefined}
                            className={classes.chip}
                            variant="outlined"
                            style={{ borderColor: "#00688B", color: "#00688B" }}
                        />
                    </li>
                );
            })}
        </Paper>
    );
}

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

const truncateString = (str: string, num: number) => {
    if (str.length <= num) {
        return str
    }
    return str.slice(0, num - 3) + "..."
}

export const Result = ({ data, screenshots }: IResultProps) => (
    <div className="card" onClick={() => outline(data)}>
        <div className="card-body">
            <h4 className="title" >{data.type === "Resource" ? "Textbook: " + data.doc_name : "Piazza: " + data.raw.history[0].subject} </h4>
            <div className="">
                <p className="description" dangerouslySetInnerHTML={{ __html: data.type === "Resource" ? truncateString(data.raw, 300) : truncateString(data.raw.history[0].content, 300) }} ></p>
            </div>
            <div className="concepts">
                <ChipsArray {...data.concepts} />
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
