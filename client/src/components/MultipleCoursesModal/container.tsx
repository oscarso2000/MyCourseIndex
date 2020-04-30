import * as React from 'react';
import { Modal } from './Modal';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import Corncis from '../../images/cornell-cis.jpg';
import { setCourseSelected } from '../../actions/index';

const useStyles = makeStyles({
  root: {
    float: "right",
    maxWidth: 245,
    height: 220,
  },
  media: {
    height: 165,
    width: 175,
    paddingRight: "30"
  },

});

const MediaCard: React.FC<{ course: any }> = ({ course }) => {
  const classes = useStyles();
  const [isShown, setIsShown] = React.useState(false);
  const modal = React.useRef<HTMLDivElement>(null);
  const closeButton = React.useRef<HTMLDivElement>(null);
  var scroll = document.querySelector('html');
  var submitted_token = "";
  const toggleScrollLock = () => {
    scroll!.classList.toggle('scroll-lock');
  };
  const someFunc = () => {
    if (course.protected) {
      console.log("am i gere rn ");
      showModal();
    }
    else {
      setCourseSelected(course.courseName);
      closeModal();

    }
  }
  const showModal = () => {
    setIsShown(true);
    if (closeButton.current) {
      closeButton.current.focus();
    }
    toggleScrollLock();
  };
  const closeModal = () => {
    setIsShown(false);
    toggleScrollLock();
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
    console.log(event.target.Token.value);
    submitted_token = event.target.Token.value;
    if (submitted_token === "12345") {
      setCourseSelected(course.courseName);
      closeModal();
    }
    else {
      console.log("wrong");
    }
  }
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
    <Card className={classes.root} onClick={someFunc}>
      <CardActionArea>
        <CardMedia
          className={classes.media}
          image={Corncis}
        />
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

  </React.Fragment >
  );
}
export default MediaCard;