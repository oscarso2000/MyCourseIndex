import {
  useHistory,
  useLocation
} from "react-router-dom";

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Corncis from '../images/cornell-cis.jpg';
import { Link } from 'react-router-dom';
import React from 'react';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import qs from 'qs';
import { setCourseSelected } from '../actions/index';

const useStyles = makeStyles({
  root: {
    maxWidth: 245,
    maxHeight: 63,
    marginBottom: 20,
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
        <CardContent className={classes.root}>
          <Typography gutterBottom variant="h5" component="h2">
            {course.courseName}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card></Link>
  );
}
export default Mediacardnomodal;