import React, { Component, useCallback } from "react";
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
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import NativeSelect from "@material-ui/core/NativeSelect";
import Container from "@material-ui/core/Container";
import { DropzoneAreaBase } from "material-ui-dropzone";
import { withRouter } from "react-router-dom";

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
      open: false,
      given_file: "aaaa",
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    // this.handleUpload = this.handleUpload.bind(this);
  }

  handleChange(event) {
    console.log("Change!");
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log("new submit");
    this.setState({ value: event.target.value });
    console.log(event.target.value);
    fetch("https://majors-fair.herokuapp.com/api/", {
      method: "POST",
      // mode:"no-cors",
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      // body: JSON.stringify({
      //   value: event.target.value
      //   // file: this.state.post
      // }),
    })
      //issue request from fromtend to backend
      .then((response) => {
        console.log(response);
        const contentType = response.headers.get('Content-Type');
        console.log(contentType);
        return response.json();
      })
      .then((data) => {
        console.log("Here!")
        this.setState({ post: data });
        this.setState({ gotmajors_flag: true });
      });
    console.log("HandleSubmit complete.")
  }

  // handleUpload(fileObj) {
  //   console.log("Uploading");
  //   // data.append("name", event.target.fil);
  //   console.log(JSON.stringify(fileObj));

  //   fetch("/api/upload/", {
  //     method: "POST",
  //     headers: {
  //       "Content-type": "multipart/form-data",
  //     },
  //     body: fileObj,
  //   })
  //     //issue request from fromtend to backend
  //     .then((response) => response.json())
  //     .then((data) => {
  //       this.setState({ post: data });
  //     });
  // }

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
            <TableCell align="right">{name}<br></br></TableCell>
            <TableCell align="right">{majors}<br></br></TableCell>
            <TableCell align="right">{links}<br></br></TableCell>
            <TableCell align="right">{minors}<br></br></TableCell>
            <TableCell align="right">{cats}<br></br></TableCell>
            <TableCell align="right">{dawgs}<br></br></TableCell>
          </TableBody>
        );
      }
    }

    return (
      <Container maxWidth="lg" justify="center">
        <Card>
          <CardContent>
            <div align="center">
              <Typography variant="h3">
                Majors Fair Excel Data Parser
              </Typography>
              <Typography variant="caption">
                The table populates correctly based on the latest "Masterlist"
                excelsheet but may need to be double-checked for accuracy.
              </Typography>
              {/* 
              <Typography variant="h6">Upload file:</Typography>
              <DropzoneAreaBase height="10%"
                acceptedFiles={[".xlsx"]}
                filesLimit={1}
                enctype="multipart/form-data"
                dropzoneText="Drop your Excel file here"
                onAdd={(fileobj) => {
                  console.log("onAdd", fileobj);
                  this.handleUpload(fileobj);
                }}
              >
              </DropzoneAreaBase> */}
            </div>
            <div align="center">
              <FormControl variant="outlined" action="">
                <NativeSelect
                  multiple={false}
                  value={this.state.value}
                  onChange={this.handleSubmit}
                >
                  <option selected value="N/A">
                    Choose one...
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
                <FormHelperText htmlFor="age-native-helper">
                  Please select a category
                </FormHelperText>
              </FormControl>
            </div>

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
                    <StyledTableCell align="center">
                      Meeting Room
                    </StyledTableCell>
                    <StyledTableCell align="center">Minors</StyledTableCell>
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
