import React, { Component } from 'react';
import Relay from 'react-relay';
import Footer from './Footer';
import Header from './Header';
import AboutUs from './AboutUs';
import LandingPage from './LandingPage';

function range(start, count) {
  return Array.apply(0, new Array(count))
    .map((element, index) => {
      return index + start;
    });
}


class App extends Component {
  static propTypes = {
    children: React.PropTypes.any,
  };
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


export default Relay.createContainer(App, {
  fragments: {}
});
