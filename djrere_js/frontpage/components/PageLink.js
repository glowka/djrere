import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import AddPageCommentMutation from '../mutations/AddPageComment';
import PageComment from './PageComment';
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
