import * as React from 'react';
import { Modal } from './Modal';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import Corncis from '../../images/cornell-cis.jpg';
import { setCourseSelected, accessProtectedCourse } from '../../actions/index';
import { Redirect } from 'react-router-dom';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert, { AlertProps } from '@material-ui/lab/Alert';
import {
  useLocation,
  useHistory
} from "react-router-dom";
import qs from 'qs';

const useStyles = makeStyles({
    root: {
        // float: "right",
        maxWidth: 245,
        height: 63,
    },
    media: {
        height: 165,
        width: 175,
        paddingRight: "30"
    },

});

const MediaCard: React.FC<{ course: any }> = ({ course }) => {
    const classes = useStyles();
    //   const classes2 = useStyles2();
    const [isShown, setIsShown] = React.useState(false);
    const [allowRedirect, setAllowRedirect] = React.useState(false);
    const [badAlert, setBadAlert] = React.useState(false);
    const modal = React.useRef<HTMLDivElement>(null);
    const closeButton = React.useRef<HTMLDivElement>(null);
    var scroll = document.querySelector('html');
    var temp = false;
    var submitted_token = "";
  
    //const toggleScrollLock = () => {
    //    scroll!.classList.toggle('scroll-lock');
    //};
  
    let location = useLocation();
    let courseInURL = qs.parse(location.search)["course"]
    
    const showModal = () => {
        setIsShown(true);
        if (closeButton.current) {
            closeButton.current.focus();
        }
        //toggleScrollLock();
    };
    const closeModal = () => {
        setIsShown(false);
        //toggleScrollLock();

    };
    const onKeyDown = (event: any) => {
        if (event.keyCode === 27) {
            closeModal();
        }
    };
    const onClickOutside = (event: any) => {
        if (modal && modal.current!.contains(event.target)) return;
        closeModal();
    };
    const onSubmit = (event: any) => {
        event.preventDefault(event);
        setCourseSelected(course.courseName);

        submitted_token = event.target.Token.value;
        const namePromise = accessProtectedCourse(submitted_token);
        namePromise.then((value) => {
            if (value) {
                setAllowRedirect(true);
            }
            else {
                closeModal();
                setBadAlert(true);
            }
            closeModal();
        })
    }
    function Alert(props: AlertProps) {
        return <MuiAlert elevation={6} variant="filled" {...props} />;
    }
    const handleClose = (event?: React.SyntheticEvent, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }

        setBadAlert(false);
    };
    const SampleModal =
        (
            <Modal
                onSubmit={onSubmit}
                modalRef={modal}
                buttonRef={closeButton}
                closeModal={closeModal}
                onKeyDown={onKeyDown}
                onClickOutside={onClickOutside}
            />
        )

    return (<React.Fragment>
        <Card className={classes.root} onClick={showModal}>
            <CardActionArea>
                {/* <CardMedia
          className={classes.media}
          image={Corncis}
        /> */}
                <CardContent className={classes.media}>
                    <Typography gutterBottom={false} variant="h5" component="h2" align="justify">
                        {course.courseName}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
        {<div>
            {isShown ? SampleModal : null}
        </div>}
        {

            (allowRedirect) ?
                (courseInURL === course.courseName ? 
                    <Redirect to={"/browse"+location.search}></Redirect>
                    : <Redirect to={"/browse"}></Redirect>
            ) :
                <div style={{ fontSize: "40px" }}>
                    <Snackbar open={badAlert} autoHideDuration={6000} onClose={handleClose}>
                        <Alert onClose={handleClose} severity="error">
                            Wrong Token! Please Try again
                        </Alert>
                    </Snackbar>
                </div>
        }
    </React.Fragment >
    );
}
export default MediaCard;
