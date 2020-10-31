import React, { Component } from 'react';
class Majors extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      value: "N/A"
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }
  handleSubmit(event) {
    event.preventDefault();
    const data = { value: this.state.value };
    console.log("submit");
    fetch("/api/",
      {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-type": "application/json",
        },
      })
      //issue request from fromtend to backend
      .then(res => res.json())
      .then(res => console.log(this.state));
    };
    
render() {
  return (
    <form action="" onSubmit={this.handleSubmit}>
      <label>Select a category: </label>
      <select multiple={false} value={this.state.value} onChange={this.handleChange}>
        <option selected value="all">All</option>
        <option value="creative">Creative</option>
        <option value="culture">Culture</option>
        <option value="asgs">Aghhh</option>
      </select>
      <input type="submit" value="Submit" />
    </form>
  );
}
}

export default Majors;