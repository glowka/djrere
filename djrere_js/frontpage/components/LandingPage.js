import React, { Component } from 'react';
import Relay from 'react-relay';
import FrontLink from './FrontLink';


class LandingPage extends Component {
  static propTypes = {
    allFrontLinks: React.PropTypes.object.isRequired,
    children: React.PropTypes.any
  };

  render() {
    return (
      <div>
        Hi there on LP!<br/>
        {this.props.allFrontLinks.edges.map(
          ({ node: link }) => <FrontLink frontLink={link} key={link.id}/>
        )}
        {this.props.children}
      </div>
    );
  }
}

export default Relay.createContainer(LandingPage, {
  fragments: {
    allFrontLinks: () => Relay.QL`
      fragment on FrontLinkDefaultConnection {
        edges {
          node {
            id,
            ${FrontLink.getFragment('frontLink')}
          }
        }
      }
    `
  }
});
