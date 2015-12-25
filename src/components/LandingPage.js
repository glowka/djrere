import React, { Component } from 'react';
import Relay from 'react-relay';


class LandingPage extends Component {

  renderLinks() {
    const {allFrontLinks} = this.props;

    return allFrontLinks.edges.map(({node}) =>
      <a href={node.href}>#{node.id} {node.href}</a>
    );
  }

  render() {
    return (
      <div>
        Hi there on LP!
        {this.renderLinks()}
      </div>
    );
  }
}

export default Relay.createContainer(LandingPage, {
  fragments: {
    allFrontLinks: () => Relay.QL`
      fragment on FrontLinkDefaultConnection { edges {
        node {
          id,
          href
        }
      }
    }
    `
  }
});

