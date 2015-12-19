import React, { Component } from 'react';

function range(start, count) {
  return Array.apply(0, Array(count))
    .map(function (element, index) {
      return index + start;
    });
}


export default class App extends Component {
  render() {
    return (
      <div>
        App running
      </div>
    );
  }
}
