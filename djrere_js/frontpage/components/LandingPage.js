import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import PageLink from './PageLink';
import AddPageLinkMutation from '../mutations/AddPageLink';
import DeletePageLinkMutation from '../mutations/DeletePageLink';


class LandingPage extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired,
    children: React.PropTypes.any
  };
  state = { inputValue: '' };

  onInputKeyDown = (event) => {
    if (event.keyCode === keycode.codes.enter) {
      this.addPageLink({ inputValue: event.target.value });
      this.setState({ inputValue: '' });
    }
  };

  onChange = (event) => {
    this.setState({ inputValue: event.target.value });
  };

  addPageLink({ inputValue }) {
    Relay.Store.commitUpdate(
      new AddPageLinkMutation({
        viewer: this.props.viewer,
        href: inputValue
      })
    );
  }

  deletePageLink({ link }) {
    Relay.Store.commitUpdate(
      new DeletePageLinkMutation({
        viewer: this.props.viewer,
        pageLink: link
      })
    );
  }

  render() {
    return (
      <div>
        Hi there on LP!
        <input
          placeholder="Add link"
          onKeyDown={this.onInputKeyDown.bind(this)}
          onChange={this.onChange.bind(this)}
          value={this.state.inputValue}
        />
        {this.props.viewer.allPageLinks.edges.map(
          ({ node: link }) =>
            <PageLink
              pageLink={link}
              handleDelete={this.deletePageLink.bind(this)}
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
        allPageLinks(last:100) {
          edges {
            node {
              id,
              ${PageLink.getFragment('pageLink')},
              ${DeletePageLinkMutation.getFragment('pageLink')}
            }
          }
        },
        ${AddPageLinkMutation.getFragment('viewer')},
        ${DeletePageLinkMutation.getFragment('viewer')}
      }
    `
  }
});
