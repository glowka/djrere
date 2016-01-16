import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import FrontLink from './FrontLink';
import AddFrontLinkMutation from '../mutations/AddFrontLink';


class LandingPage extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired,
    children: React.PropTypes.any
  };
  state = { inputValue: '' };

  onInputKeyDown = (event) => {
    if (event.keyCode === keycode.codes.enter) {
      this.addComment({ inputValue: event.target.value });
      this.setState({ inputValue: '' });
    }
  };

  onChange = (event) => {
    this.setState({ inputValue: event.target.value });
  };

  addComment({ inputValue }) {
    Relay.Store.commitUpdate(
      new AddFrontLinkMutation({
        viewer: this.props.viewer,
        href: inputValue
      })
    );
  }

  render() {
    return (
      <div>
        Hi there on LP!<br/>
        {this.props.viewer.allFrontLinks.edges.map(
          ({ node: link }) => <FrontLink frontLink={link} key={link.id}/>
        )}
        <input
          onKeyDown={this.onInputKeyDown}
          onChange={this.onChange}
          value={this.state.inputValue}
        />
        {this.props.children}
      </div>
    );
  }
}

export default Relay.createContainer(LandingPage, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
        allFrontLinks(last:100) {
          edges {
            node {
              id,
              ${FrontLink.getFragment('frontLink')}
            }
          }
        },
        ${AddFrontLinkMutation.getFragment('viewer')}
      }
    `
  }
});
