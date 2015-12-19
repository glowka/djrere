import React, { Component } from 'react';
import Footer from './Footer';
import Header from './Header';
import AboutUs from './AboutUs';
import LandingPage from './LandingPage';

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
        <Header />
          {this.props.children}
        <Footer />
      </div>
    );
  }
}
