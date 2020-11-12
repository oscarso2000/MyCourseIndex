import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import { Link } from 'react-router-dom';
import React from 'react';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
    root: {
        maxWidth: 245,
        maxHeight: 63,
        marginBottom: 20,
    },
});

const AddCourseCard: React.FC<{ course: any }> = ({ course }) => {
    const classes = useStyles();
    return (
        <Link to={"/form"}><Card className={classes.root}>
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
export default AddCourseCard;
