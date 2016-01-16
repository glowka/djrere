import keycode from 'keycode';
import React, { Component } from 'react';
import Relay from 'react-relay';
import AddCommentMutation from '../mutations/AddComment';
import Comment from './Comment';
import './FrontLink.less';


class FrontLink extends Component {
  static propTypes = {
    frontLink: React.PropTypes.object.isRequired
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
      new AddCommentMutation({
        frontLink: this.props.frontLink,
        content: inputValue
      })
    );
  }

  render() {
    const { frontLink } = this.props;
    return (
      <div className="FrontLink-wrapper">
        <a href={frontLink.href}>Link to <b>{frontLink.href}</b> with #{frontLink.id}</a>
        {this.props.frontLink.comments.edges.map(
          ({ node: comment }) => <Comment comment={comment} key={comment.id} />
        )}
        <input
          onKeyDown={this.onInputKeyDown}
          onChange={this.onChange}
          value={this.state.inputValue}
        />
      </div>
    );
  }
}


export default Relay.createContainer(FrontLink, {
  fragments: {
    frontLink: () => Relay.QL`
      fragment on FrontLink {
        id,
        href,
        comments(last: 10) {
          edges {
            node {
              ${Comment.getFragment('comment')}
            }
          }
        },
        ${AddCommentMutation.getFragment('frontLink')}
      }
    `
  }
});
