import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import Corncis from '../images/cornell-cis.jpg';
import { setCourseSelected } from '../actions/index';
import { Link } from 'react-router-dom';
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

const Mediacardnomodal: React.FC<{ course: any }> = ({ course }) => {
  const classes = useStyles();
  let location = useLocation();
  let courseInURL = qs.parse(location.search)["course"]
  return (
    <Link to={(courseInURL === course.courseName ? "/browse"+location.search : "/browse")}><Card className={classes.root} onClick={() => setCourseSelected(course.courseName)}>
      <CardActionArea>
        {/* <CardMedia
          className={classes.media}
          image={Corncis}
        /> */}
        <CardContent className={classes.media} >
          <Typography gutterBottom variant="h5" component="h2">
            {course.courseName}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card></Link>
  );
}
export default Mediacardnomodal;