import '../style/ResultsView.css';

import * as React from 'react';

import { Theme, ThemeProvider, WithStyles, createStyles, makeStyles, withStyles } from '@material-ui/core/styles';
import { handleKey1, search1, setOrder, setQuery, setSearchSel, setTags } from '../actions';
import {
  useHistory,
  useLocation
} from "react-router-dom";

import Autocomplete from '@material-ui/lab/Autocomplete';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import CloseIcon from '@material-ui/icons/Close';
import Dialog from '@material-ui/core/Dialog';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormGroup from '@material-ui/core/FormGroup';
import IconButton from '@material-ui/core/IconButton';
import { Link } from 'react-router-dom';
import { Loader } from './Loader';
import MuiDialogActions from '@material-ui/core/DialogActions';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { Outline } from './Outline';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import { ResultsList } from './ResultsList';
import Switch from '@material-ui/core/Switch';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import { createMuiTheme } from '@material-ui/core/styles';
import cyan from '@material-ui/core/colors/cyan';
import glass from '../images/glass.svg';
import grey from '@material-ui/core/colors/grey';
import qs from 'qs';
import styled from 'styled-components';

const blk = grey[900];
const cyn = cyan[400];

const theme1 = createMuiTheme({
    palette: {
        secondary: {
            light: '#00CDCD',
            main: '#00688B',
        },
    },
});

const styles = (theme: Theme) =>
    createStyles({
        root: {
            //   margin: 0,
            //   padding: theme.spacing(2),
        },
        closeButton: {
            position: 'absolute',
            right: theme.spacing(1),
            top: theme.spacing(1),
            color: theme.palette.grey[500],
        },
    });

export interface DialogTitleProps extends WithStyles<typeof styles> {
    id: string;
    children: React.ReactNode;
    onClose: () => void;
}

const DialogTitle = withStyles(styles)((props: DialogTitleProps) => {
    const { children, classes, onClose, ...other } = props;
    return (
        <MuiDialogTitle disableTypography className={classes.root} {...other}>
            <Typography variant="h6">{children}</Typography>
            {onClose ? (
                <IconButton aria-label="close" className={classes.closeButton} onClick={onClose}>
                    <CloseIcon />
                </IconButton>
            ) : null}
        </MuiDialogTitle>
    );
});

const DialogContent = withStyles((theme: Theme) => ({
    root: {
        padding: theme.spacing(2),
    },
}))(MuiDialogContent);

const DialogActions = withStyles((theme: Theme) => ({
    root: {
        margin: 0,
        padding: theme.spacing(1),
    },
}))(MuiDialogActions);

const useStyles = makeStyles((theme: Theme) =>
    createStyles({
        root: {
            width: 350,
            '& > * + *': {
                marginTop: theme.spacing(3),
            },
        },
    }),
);


export const ResultsView: React.StatelessComponent<any> = ({ results, outline, screenshots, query, loadingStatus, order, search, folders, tags, QA}: any): JSX.Element => {
    const mobile: string[] = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry'];
    const ASC = 'ascending';
    const DSC = 'descending';

    let history= useHistory();
    let location = useLocation();
    let urlQuery= qs.parse(location.search)["?query"]

    var results1 = results;

    const folders1: string[] = folders;

    const sortByTimestamp = (a: any, b: any, sortOrder: any = DSC) => {
        // console.log(a);
        const diff = a.timestamp.toLowerCase().localeCompare(b.timestamp.toLowerCase());

        if (sortOrder === ASC) {
            return diff;
        }
        return -1 * diff;
    }


    const sortByScore = (a: any, b: any, sortOrder: any = DSC) => {
        const diff = a.score - b.score;

        if (sortOrder === ASC) {
            return diff;
        }
        return -1 * diff;
    }

    function sortPiazza(a: any) {
        return (a.type === "Piazza");
    }

    function sortResource(a: any) {
        return (a.type === "Resource");
    }

    function sortTags(a: any) { //variable tags, and a.raw.folders
        return (a.type === "Resource" || (a.type === "Piazza" && ((tags.filter((value: string) => a.raw.folders.includes(value))).length > 0))) //value noimplicitany
    }

    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    const handleChange = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        //ordered sort
        setOrder(!order);
    };

    // console.log(tags);
    // console.log(results);

    if (typeof results === 'undefined') {
        results = [];
    }

    if (search === "Default") {
        // results1 = results;
        if (tags.length !== 0) {
            results1 = results.filter(sortTags);
            console.log(results1);
        } else {
            results1 = results;
        }
    } else if (search === "Piazza") {
        // results1 = results.filter(sortPiazza);
        if (tags.length !== 0) {
            results1 = results.filter(sortTags).filter(sortPiazza);
        } else {
            results1 = results.filter(sortPiazza);
        }
    } else if (search === "Resource") {
        // results1 = results.filter(sortResource);
        if (tags.length !== 0) {
            results1 = results.filter(sortTags).filter(sortResource);
        } else {
            results1 = results.filter(sortResource);
        }
    }

    // if (tags.length != 0){
    //   results1 = results1.filter(sortTags);
    // }else{
    //   results1 = results1;
    // }

    if (results && results.length > 0) {
        if (order) {
            results1.sort((a: any, b: any) => sortByTimestamp(a, b));
        } else {
            results1.sort((a: any, b: any) => sortByScore(a, b));
        }
    }
    const classes = useStyles();

    return (
        <div>
            <div className="top-bar">
                <Link className="header" to="/" target="_self" style={{ textDecoration: "none"}}>
                    <h3 className="heading-1">MyCourseIndex</h3>
                    <h3 className="heading-2">Courses</h3>
                </Link>
                <input
                    defaultValue={urlQuery as string}
                    onKeyPress={e => handleKey1(e,history, 'reset')}
                    onChange={e => setQuery(e)}
                />
                <img onClick={() => search1(history,'reset')} className="glass" alt="magnifying glass" src={glass} />
                <div className="filters">
                    <ThemeProvider theme={theme1}>
                        <Button variant="contained" color="secondary" onClick={handleClickOpen}>
                            Filter By
                        </Button>
                        <Dialog onClose={handleClose} aria-labelledby="customized-dialog-title" open={open}>
                            <DialogTitle id="customized-dialog-title" onClose={handleClose}>
                                <Box fontWeight="fontWeightBold" fontSize={23}>
                                    Advanced Filters
                          </Box>
                            </DialogTitle>
                            <DialogContent dividers>
                                <Typography gutterBottom>
                                    Sort:
                          </Typography>
                                <ThemeProvider theme={theme1}>
                                    <FormControlLabel
                                        control={<Switch
                                            checked={order}
                                            onClick={handleChange}
                                            name="checkedB"
                                            color="secondary" //to change also radio group below
                                        />}
                                        label="Sort by Most Recent" />
                                </ThemeProvider>
                                <Typography gutterBottom>
                                    Resource Filter:
                          </Typography>
                                <ThemeProvider theme={theme1}>
                                    <RadioGroup aria-label="SearchFilters" color="secondary" name="gender1" onChange={(e: any) => setSearchSel(e)}>
                                        <FormControlLabel value="Default" control={<Radio />} label="Search All" checked={search === "Default"} />
                                        <FormControlLabel value="Piazza" control={<Radio />} label="Search Piazza Only" checked={search === "Piazza"} />
                                        <FormControlLabel value="Resource" control={<Radio />} label="Search Resources Only" checked={search === "Resource"} />
                                    </RadioGroup>
                                </ThemeProvider>
                                <Typography gutterBottom>
                                    Piazza Folders:
                          </Typography>
                                <div className={classes.root}>
                                    <Autocomplete
                                        multiple
                                        id="tags-standard"
                                        options={folders1}
                                        defaultValue={tags}
                                        onChange=
                                        {
                                            (e: any, value: any) => setTags(e, value)
                                        }
                                        getOptionLabel={(option: any) => option}
                                        renderInput={(params: any) => (
                                            <TextField
                                                {...params}
                                                variant="standard"
                                                placeholder="Add Labels"
                                            />
                                        )}
                                    />
                                </div>
                            </DialogContent>
                            <DialogActions>
                                <Button autoFocus onClick={handleClose} color="secondary">
                                    Save changes
                        </Button>
                            </DialogActions>
                        </Dialog>
                    </ThemeProvider>
                </div>
                <div className="help-tip2">
                    <p><b>For Advanced Searches:</b><br />1) +’query’ for mandatory inclusion.<br />2) -’query’ for mandatory exclusion.<br />3) ‘query^n to emphasize n times. </p>
                </div>
                <Link to="/about" className="about-bar" style={{ textDecoration: "none" }}>
                    About
                </Link>
            </div>
            <Outline outline={outline} />
            {loadingStatus === true
                ? <div className={mobile.includes(navigator.platform) ? "" : "load-wrap"}><Loader /></div>
                : <ResultsList results={results1} screenshots={screenshots} QA={QA}/>
            }
        </div>
    );
};