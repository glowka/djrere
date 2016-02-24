import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import AddPageCommentMutation from '../mutations/AddPageComment';
import PageComment from './PageComment';

import { fixObjKey } from '../../utils/relay-fixes';

import './PageLink.less';


class PageLink extends Component {
  static propTypes = {
    pageLink: React.PropTypes.object.isRequired,
    handleDelete: React.PropTypes.func.isRequired
  };
  state = { inputValue: '' };

  onInputKeyDown = (event) => {
    if (event.keyCode === keycode.codes.enter) {
      this.addPageComment({ inputValue: event.target.value });
      this.setState({ inputValue: '' });
    }
  };

  onChange = (event) => {
    this.setState({ inputValue: event.target.value });
  };

  addPageComment({ inputValue }) {
    Relay.Store.commitUpdate(
      new AddPageCommentMutation({
        pageLink: this.props.pageLink,
        content: inputValue
      })
    );
  }

  fixRelayProps(props) {
    // Looks like relay is buggy here, fixing by setting proper key
    fixObjKey(props.pageLink, 'pageComments')
  }

  componentWillMount() {
    this.fixRelayProps(this.props)
  }

  componentWillUpdate(nextProps, nextState) {
    this.fixRelayProps(nextProps)
  }


  render() {
    const { pageLink } = this.props;
    return (
      <div className="PageLink-wrapper">
        <a href={pageLink.href}>Link to <b>{pageLink.href}</b> with #{pageLink.id}</a>
        <span onClick={() => this.props.handleDelete({ link: pageLink })}>delete me</span>
        {this.props.pageLink.pageComments.edges.map(
          ({ node: pageComment }) => <PageComment pageComment={pageComment} key={pageComment.id} />
        )}
        <input
          placeholder="Add pageComment"
          onKeyDown={this.onInputKeyDown.bind(this)}
          onChange={this.onChange.bind(this)}
          value={this.state.inputValue}
        />
      </div>
    );
  }
}


export default Relay.createContainer(PageLink, {
  fragments: {
    pageLink: () => Relay.QL`
      fragment on PageLink {
        id,
        href,
        pageComments(last: 10) {
          edges {
            node {
              ${PageComment.getFragment('pageComment')}
            }
          }
        },
        ${AddPageCommentMutation.getFragment('pageLink')},
      }
    `
  }
});
