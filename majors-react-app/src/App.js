import React from "react";
import "fontsource-roboto";
import Card from "@material-ui/core/Card";
import Typography from "@material-ui/core/Typography";
import CardContent from "@material-ui/core/CardContent";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Alert from "@material-ui/lab/Alert";
import Majors from "./Majors";
import { Switch, Route, Redirect } from "react-router-dom";
import ReactDOM from 'react-dom';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { username: "", password: "", redirect: false };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({
      username: event.state.username,
      password: event.state.password,
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log("submit");
    console.log(this.state.username);
    console.log(this.state.password);

    if (this.state.username == "admin" && this.state.password == "uga24") {
      this.state.redirect = true;
      console.log("We made it!");
   
ReactDOM.render(
  <Majors />,
  document.getElementById('root')
);
      
    }
  }

  render() {
    return (
      <Grid
  container
  spacing={0}
  direction="row"
  alignItems="center"
  justify="center"
  style={{ minHeight: '100vh' }}
>
        <Grid item xs={3}>
          <div text-align="center">
            <Typography variant="h4">
              Please enter a login for access:
            </Typography>
            <TextField
              type="username"
              id="standard-basic"
              placeholder="Username"
              fullWidth
              name="username"
              variant="outlined"
              value={this.state.username}
              onChange={(event) =>
                this.setState({
                  [event.target.name]: event.target.value,
                })
              }
            />

            <TextField
              id="standard-basic"
              type="password"
              placeholder="Password"
              fullWidth
              name="password"
              variant="outlined"
              value={this.state.password}
              onChange={(event) =>
                this.setState({
                  [event.target.name]: event.target.value,
                })
              }
            />
            <Button
              onClick={(event) => {
                this.handleSubmit(event);
              }}
              variant="contained"
              color="primary"
              type="submit"
            >
              Submit
            </Button>
            </div>
        </Grid>
      </Grid>
    );
  }
}
export default App;
