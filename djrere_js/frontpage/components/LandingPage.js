import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import FrontLink from './FrontLink';
import AddFrontLinkMutation from '../mutations/AddFrontLink';
import DeleteFrontLinkMutation from '../mutations/DeleteFrontLink';


class LandingPage extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired,
    children: React.PropTypes.any
  };
  state = { inputValue: '' };

  onInputKeyDown = (event) => {
    if (event.keyCode === keycode.codes.enter) {
      this.addFrontLink({ inputValue: event.target.value });
      this.setState({ inputValue: '' });
    }
  };

  onChange = (event) => {
    this.setState({ inputValue: event.target.value });
  };

  addFrontLink({ inputValue }) {
    Relay.Store.commitUpdate(
      new AddFrontLinkMutation({
        viewer: this.props.viewer,
        href: inputValue
      })
    );
  }


  deleteFrontLink({ link }) {
    Relay.Store.commitUpdate(
      new DeleteFrontLinkMutation({
        viewer: this.props.viewer,
        frontLink: link
      })
    );
  }

  render() {
    return (
      <div>
        Hi there on LP!
        <input
          placeholder="Add link"
          onKeyDown={this.onInputKeyDown}
          onChange={this.onChange}
          value={this.state.inputValue}
        />
        {this.props.viewer.allFrontLinks.edges.map(
          ({ node: link }) =>
            <FrontLink
              frontLink={link}
              handleDelete={this.deleteFrontLink.bind(this)}
              key={link.id}
            />
        )}
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
              ${FrontLink.getFragment('frontLink')},
              ${DeleteFrontLinkMutation.getFragment('frontLink')}
            }
          }
        },
        ${AddFrontLinkMutation.getFragment('viewer')},
        ${DeleteFrontLinkMutation.getFragment('viewer')}
      }
    `
  }
});
