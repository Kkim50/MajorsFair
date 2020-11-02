import React, { Component } from "react";
import "fontsource-roboto";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { withStyles, makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import Typography from "@material-ui/core/Typography";
import CardContent from "@material-ui/core/CardContent";
import InputLabel from "@material-ui/core/InputLabel";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import NativeSelect from '@material-ui/core/NativeSelect';
import Container from '@material-ui/core/Container';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';


const useStyles = makeStyles({
  root: {
    minWidth: 275,
    maxWidth: 500,
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

class Majors extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "N/A",
      post: null,
      gotmajors_flag: false,
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log("submit");
    fetch("/api/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        value: this.state.value,
      }),
    })
      //issue request from fromtend to backend
      .then((response) => response.json())
      .then((data) => {
        this.setState({ post: data });
        this.setState({ gotmajors_flag: true });
      });
  }

  render() {
    const post = this.state.post;
    const value = this.state.value;
    var category = null;
    var majors_data = [];
    if (this.state.gotmajors_flag) {
      category = post[value];
      for (var person in category) {
        var person_data = category[person];
        var name = person;
        var links = person_data["Zoom Link"];
        var majors = person_data["Majors"];
        var minors = person_data["Minors"];
        var cats = person_data["Certificates"];
        var dawgs = person_data["Double Dawgs / Double Majors"];

        majors_data.push(
          <TableBody>
            <TableCell align="right">{name}</TableCell>
            <TableCell align="right">{majors}</TableCell>
            <TableCell align="right">{links}</TableCell>
            <TableCell align="right">{minors}</TableCell>
            <TableCell align="right">{cats}</TableCell>
            <TableCell align="right">{dawgs}</TableCell>
          </TableBody>
        );
      }
    }

    return (
<Container maxWidth="lg" justify="center">
        <Card>
          <CardContent>
          <Grid container justify="center" spacing="1">
          <Grid item xs={4}>
              <Typography variant="h5" gutterBottom>
              Majors Fair Excel Data Parser
            </Typography>
            </Grid>
          <Grid item xs={4}>

            <FormControl variant="outlined" variant="outlined" action="">
              <NativeSelect
                multiple={false}
                value={this.state.value}
                onChange={this.handleChange}
                onClick={(e) => this.handleSubmit(e)}
              >
                <option selected value="all">
                  All
                </option>
                <option value="Creative">Creative</option>
                <option value="Culture">Culture</option>
                <option value="Life">Life</option>
                <option value="Nature">Nature</option>
                <option value="Technology">Technology</option>
                <option value="Leadership">Leadership</option>
                <option value="DoubleDawgs">
                  DoubleDawgs, FinAid, Grad School
                </option>
                <option value="Service">Service</option>
              </NativeSelect>
              <FormHelperText style={{justifyContent:'left'}} htmlFor="age-native-helper">Please select a category</FormHelperText>
            </FormControl>
            </Grid>
            </Grid>
            <TableContainer component={Paper}>
              <Table
                stickyHeader
                className="Majors Fair Excel Data Parser"
                size="small"
                aria-label="a dense table"
              >
                <TableHead>
                  <TableRow>
                  <StyledTableCell align="center">Name</StyledTableCell>
                    <StyledTableCell align="center">Majors</StyledTableCell>
                    <StyledTableCell align="center">Meeting Room</StyledTableCell>
                    <StyledTableCell align="center">
                      Minors
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      Certificates
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      Double Dawgs/ Double Majors
                    </StyledTableCell>
                  </TableRow>
                </TableHead>
                {majors_data}
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
        </Container> 
            );
  }
}

export default Majors;
