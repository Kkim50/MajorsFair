import React, { Component } from 'react';

class Majors extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "N/A",
      post: "blahhh"
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    const {formRating} = { value: this.state };
    console.log("submit");
    fetch("/api/", 
    {
      method: "POST",
      headers: {
      "Content-type": "application/json"
    },
      body: JSON.stringify({
        value: this.state.value
      })
    }) 
      //issue request from fromtend to backend
      .then(response => response.json())
      .then(data => this.setState({post: JSON.stringify(data)}))
        // this.setState({post: response.json()})
    // )
  }

  render() {
    const { post } = this.state;
    return (
      <div>
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
      <p>{post} world</p>
      </div>
    );
  }
  }

  export default Majors;