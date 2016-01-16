import React, { Component } from 'react';
import Relay from 'react-relay';

class AboutUs extends Component {
  static propTypes = {
    viewer: React.PropTypes.any,
    children: React.PropTypes.any
  };
  render() {
    return (
      <div>
        About Us
        {this.props.children}
      </div>
    );
  }
}


export default Relay.createContainer(AboutUs, {
  fragments: {}
});
