import * as React from 'react';
import { ResultsList } from './ResultsList';
import { Link } from 'react-router-dom';
import { Outline } from './Outline';
import { handleKey, search1, setQuery, setOrder, setSearchSel } from '../actions';
import '../style/ResultsView.css';
import glass from '../images/glass.svg';
import { Loader } from './Loader';
import Switch from '@material-ui/core/Switch';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { createStyles, Theme, withStyles, WithStyles, ThemeProvider} from '@material-ui/core/styles';
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
import ToggleButton from '@material-ui/lab/ToggleButton';
import grey from '@material-ui/core/colors/grey';
import cyan from '@material-ui/core/colors/cyan';
import useAutocomplete from '@material-ui/lab/useAutocomplete';
import NoSsr from '@material-ui/core/NoSsr';
import CheckIcon from '@material-ui/icons/Check';
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

  const Label = styled('label')`
  padding: 0 0 4px;
  line-height: 1.5;
  display: block;
`;

const InputWrapper = styled('div')`
  width: 300px;
  border: 1px solid #d9d9d9;
  background-color: #fff;
  border-radius: 4px;
  padding: 1px;
  display: flex;
  flex-wrap: wrap;

  &:hover {
    border-color: #40a9ff;
  }

  &.focused {
    border-color: #40a9ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  }

  & input {
    font-size: 14px;
    height: 30px;
    box-sizing: border-box;
    padding: 4px 6px;
    width: 0;
    min-width: 30px;
    flex-grow: 1;
    border: 0;
    margin: 0;
    outline: 0;
  }
`;

const Tag = styled(({ label, onDelete, ...props }) => (
  <div {...props}>
    <span>{label}</span>
    <CloseIcon onClick={onDelete} />
  </div>
))`
  display: flex;
  align-items: center;
  height: 24px;
  margin: 2px;
  line-height: 22px;
  background-color: #fafafa;
  border: 1px solid #e8e8e8;
  border-radius: 2px;
  box-sizing: content-box;
  padding: 0 4px 0 10px;
  outline: 0;
  overflow: hidden;

  &:focus {
    border-color: #40a9ff;
    background-color: #e6f7ff;
  }

  & span {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  & svg {
    font-size: 12px;
    cursor: pointer;
    padding: 4px;
  }
`;

const Listbox = styled('ul')`
  width: 300px;
  margin: 2px 0 0;
  padding: 0;
  position: absolute;
  list-style: none;
  background-color: #fff;
  overflow: auto;
  max-height: 250px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1;

  & li {
    padding: 5px 12px;
    display: flex;

    & span {
      flex-grow: 1;
    }

    & svg {
      color: transparent;
    }
  }

  & li[aria-selected='true'] {
    background-color: #fafafa;
    font-weight: 600;

    & svg {
      color: #1890ff;
    }
  }

  & li[data-focus='true'] {
    background-color: #e6f7ff;
    cursor: pointer;

    & svg {
      color: #000;
    }
  }
`;

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

const FolderButtons: React.FC<string> = (text: string) => {
  const[selected,setSelected] = React.useState(false);
  const handleToggle = () => {
    setSelected(!selected);
  }
  return (<ToggleButton
    style={{color: blk}}
    value="folder"
    selected={selected}
    onChange={handleToggle}
  > {text}
  </ToggleButton>)
}


export const ResultsView: React.StatelessComponent<any> = ({ results, outline, screenshots, query, loadingStatus, order, search, folders }: any): JSX.Element => {
    const mobile: string[] = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry'];
    const ASC = 'ascending';
    const DSC = 'descending';
    var results1 = results;

    const folders1:string[] = folders;

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
    };

    const handleChange = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        //ordered sort
        setOrder(!order);
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

    const {
      getRootProps,
      getInputProps,
      getTagProps,
      getListboxProps,
      getOptionProps,
      value,
      groupedOptions,
      focused,
      setAnchorEl,
    } = useAutocomplete({
      id: 'customized-hook-demo',
      defaultValue: [folders1[0]],
      multiple: true,
      options: folders1,
      getOptionLabel: (option) => option,
    });
    
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
                          <Typography gutterBottom>
                            Piazza Folders:
                          </Typography>
                            {/* {
                              folders.map((item: string, i: any) => FolderButtons(item))
                            } */}
                                  <div>
                                    <div {...getRootProps()}>
                                      <InputWrapper ref={setAnchorEl} className={focused ? 'focused' : ''}>
                                        {value.map((option: string, index: number) => (
                                          <Tag label={option} {...getTagProps({ index })} />
                                        ))}
                                        <input {...getInputProps()} />
                                      </InputWrapper>
                                    </div>
                                    {groupedOptions.length > 0 ? (
                                      <Listbox {...getListboxProps()}>
                                        {groupedOptions.map((option, index) => (
                                          <li {...getOptionProps({ option, index })}>
                                            <span>{option}</span>
                                            <CheckIcon fontSize="small" />
                                          </li>
                                        ))}
                                      </Listbox>
                                    ) : null}
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
