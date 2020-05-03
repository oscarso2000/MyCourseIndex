import * as React from 'react';
import { ResultsList } from './ResultsList';
import { Link } from 'react-router-dom';
import { Outline } from './Outline';
import { handleKey, search1, setQuery, setQueryString, setOrder, setSearchSel } from '../actions';
import '../style/ResultsView.css';
import glass from '../images/glass.svg';
import { Loader } from './Loader';
import Switch from '@material-ui/core/Switch';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { createStyles, Theme, withStyles, WithStyles, ThemeProvider } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogActions from '@material-ui/core/DialogActions';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Typography from '@material-ui/core/Typography';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import { createMuiTheme } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';

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

export const ResultsView: React.StatelessComponent<any> = ({ results, outline, screenshots, query, loadingStatus, order, search }: any): JSX.Element => {
    const mobile: string[] = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry'];
    const ASC = 'ascending';
    const DSC = 'descending';

    // if (!! results) {
    //     // loadingStatus = true;
    //     setQueryString("MyCourseIndex");
    // }

    var results1 = results;

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

    function sortPiazza(a:any){
        return (a.type === "Piazza");
    }

    function sortResource(a:any){
        return (a.type === "Resource");
    }

    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
      setOpen(false);
    //   search();
    //   setOrder(!order);
    };

    

    // const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    //     // event.persist();
    //     // console.log(event.target.checked);
    //     console.log("Clicked");
    //     setOrder(!order);
    // };

    const handleChange = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        // event.persist();
        // console.log(event.target.checked);
        // console.log("Clicked");

        //ordered sort
        setOrder(!order);
        //search selection
    };

    if(search === "Default"){
        results1 = results;
    }else if (search === "Piazza"){
        results1 = results.filter(sortPiazza);
    }else if (search === "Resource"){
        results1 = results.filter(sortResource);
    }

    if (results && results.length > 0) {
        if (order) {
            results1.sort((a: any, b: any) => sortByTimestamp(a, b));
        } else {
            results1.sort((a: any, b: any) => sortByScore(a, b));
        }
    }

   
    return (
        <div>
            <div className="top-bar">
                <Link to="/" target="_self" style={{ textDecoration: "none" }}>
                    <h3 className="heading-1">MyCourseIndex</h3>
                    <h3 className="heading-2">Search</h3>
                </Link>
                <input
                    defaultValue={decodeURI(query)}
                    onKeyPress={e => handleKey(e, 'reset')}
                    onChange={e => setQuery(e)}
                />
                <img onClick={() => search1('reset')} className="glass" alt="magnifying glass" src={glass} />
                <div className = "filters">
                    <ThemeProvider theme={theme1}>
                        <Button variant="contained" color="secondary" onClick={handleClickOpen}>
                            Advanced Filters
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
                        control = {<Switch
                            checked={order}
                            onClick={handleChange}
                            name="checkedB"
                            color="secondary" //to change also radio group below
                        />}
                        label = "Sort by Most Recent"/>
                        </ThemeProvider>
                        <Typography gutterBottom>
                            Resource Filter:
                        </Typography>
                        <ThemeProvider theme={theme1}>
                            <RadioGroup aria-label="SearchFilters" color = "secondary" name="gender1" onChange={e=>setSearchSel(e)}>
                                <FormControlLabel value="Default" control={<Radio />} label="Search All" checked = {search === "Default"} />
                                <FormControlLabel value="Piazza" control={<Radio />} label="Search Piazza Only" checked = {search === "Piazza"}/>
                                <FormControlLabel value="Resource" control={<Radio />} label="Search Resources Only" checked = {search === "Resource"}/>
                            </RadioGroup>
                        </ThemeProvider>
                        </DialogContent>
                        <DialogActions>
                        <Button autoFocus onClick={handleClose} color="secondary">
                            Save changes
                        </Button>
                        </DialogActions>
                    </Dialog>
                    </ThemeProvider>
                </div>

                <Link to="/about" className="about-bar" style={{ textDecoration: "none" }}>
                    About
                </Link>
            </div>
            <Outline outline={outline} />
            {loadingStatus === true
                ? <div className={mobile.includes(navigator.platform) ? "" : "load-wrap"}><Loader /></div>
                : <ResultsList results={results1} screenshots={screenshots} />
            }
        </div>
    );
};
