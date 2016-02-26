import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import PageLink from './PageLink';
import AddPageLinkMutation from '../mutations/AddPageLink';
import DeletePageLinkMutation from '../mutations/DeletePageLink';

import { fixObjKey } from '../../utils/relay-fixes';


class LandingPage extends Component {
  static propTypes = {
    user: React.PropTypes.object.isRequired,
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
    console.log(this.props.user);
    Relay.Store.commitUpdate(
      new AddPageLinkMutation({
        user: this.props.user,
        frontpage: this.props.user.frontpage,
        href: inputValue
      })
    );
  }

  deletePageLink({ link }) {
    console.log(link);
    Relay.Store.commitUpdate(
      new DeletePageLinkMutation({
        user: this.props.user,
        frontpage: this.props.user.frontpage,
        pageLink: link
      })
    );
  }

  fixRelayProps(props) {
    // Looks like relay is buggy here, fixing by setting proper key
    fixObjKey(props.user.frontpage, 'allPageLinks')
  }

  componentWillMount() {
    this.fixRelayProps(this.props)
  }

  componentWillUpdate(nextProps, nextState) {
    this.fixRelayProps(nextProps)
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
        {this.props.user.frontpage.allPageLinks.edges.map(
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
    user: () => Relay.QL`
      fragment on User {
        frontpage {
          allPageLinks(last:100) {
            edges {
              node {
                id,
                ${PageLink.getFragment('pageLink')},
                ${DeletePageLinkMutation.getFragment('pageLink')}
              }
            }
          }
          ${AddPageLinkMutation.getFragment('frontpage')}
          ${DeletePageLinkMutation.getFragment('frontpage')}
        }
        ${AddPageLinkMutation.getFragment('user')}
        ${DeletePageLinkMutation.getFragment('user')}
      }
    `
  }
});
