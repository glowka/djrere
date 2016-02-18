import React, { Component } from 'react';
import Relay from 'react-relay';
import Footer from './Footer';
import Header from './Header';


class Blog extends Component {
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


export default Relay.createContainer(Blog, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
        blog {
          articleNode { id }
        }
      }
    `
  }
});
