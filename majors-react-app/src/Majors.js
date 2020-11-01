import React, { Component } from "react";
import Table from 'react-bootstrap/Table';

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
    const { formRating } = { value: this.state };
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
        var person_data = category[person]
        var links = person_data['Zoom Link'];
        var majors = person_data["Majors"];
        var minors = person_data["Minors"];
        var cats = person_data["Certificates"];
        var dawgs = person_data["Double Dawgs \/ Double Majors"];

        majors_data.push(
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Major</th>
                <th>Meeting Room</th>
                <th>Minor</th>
                <th>Certificate</th>
                <th>Double Dawgs/Dual Degree</th>
                </tr> </thead>
        <tbody>
        <tr>
        <td>{majors}</td>
        <td><a href={links}><span>{links}</span></a></td>
        <td>{minors}</td>
        <td><span>{cats}</span></td>
        <td>{dawgs}</td>
        </tr>
        </tbody>
        </Table>
        );
      }
    }

    return (
      <div>
        <form action="" onSubmit={this.handleSubmit}>
          <label>Select a category: </label>
          <select
            multiple={false}
            value={this.state.value}
            onChange={this.handleChange}
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
          </select>
          <input type="submit" value="Submit" />
        </form>
        <p>
          <div>
            <p>{majors_data}</p>
          </div>
        </p>
      </div>
    );
  }
}

export default Majors;
