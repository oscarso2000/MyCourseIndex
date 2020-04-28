import * as React from 'react';
import { Modal } from './Modal';
import TriggerButton from './TriggerButton';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Magd from '../../images/Magd_Bayoumi.png';

const useStyles = makeStyles({
  root: {
    maxWidth: 345,
  },
  media: {
    height: 140,
  },
});

const MediaCard: React.FC = (course: any) => {
  const classes = useStyles();
  const [isShown, setIsShown] = React.useState(false);
  const closeButton = React.createRef();
  const modal = React.createRef();
  const toggleScrollLock = () => {
    //@ts-ignore
    document.querySelector('html').classList.toggle('scroll-lock');
  };
  const showModal = () => {
    setIsShown(true);
    if (closeButton.current) {
      //@ts-ignore
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
    //@ts-ignore
    if (modal && modal.current.contains(event.target)) return;
    closeModal();
  };
  const onSubmit = (event: any) => {
    console.log(event);
  }
  const SampleModal = React.forwardRef((props, ref) => {
    //@ts-ignore
    const { ref1, ref2 } = ref;
    return (
      <Modal
        onSubmit={onSubmit}
        modalRef={ref1}
        buttonRef={ref2}
        closeModal={closeModal}
        onKeyDown={onKeyDown}
        onClickOutside={onClickOutside}
      />
    )
  }
  );
  return (
    <React.Fragment>
      <Card className={classes.root} onClick={showModal}>
        <CardActionArea>
          {/* <CardMedia
            className={classes.media}
            image={Magd}
          /> */}
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              {(course.course.courseName)}
            </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
      {/* 
      //@ts-ignore */}
      {isShown ? <SampleModal ref={{ ref1: modal, ref2: closeButton }} /> : null}
    </React.Fragment>
  );
}

export default MediaCard;