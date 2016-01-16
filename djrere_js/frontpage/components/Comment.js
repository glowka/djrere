import React, { Component } from 'react';
import Relay from 'react-relay';
import './Comment.less';


class Comment extends Component {
  static propTypes = {
    comment: React.PropTypes.object.isRequired,
  };

  render() {
    const { comment } = this.props;

    return (
      <div className="Comment-wrapper">{comment.content}</div>
    );
  }
}


export default Relay.createContainer(Comment, {
  fragments: {
    comment: () => Relay.QL`
      fragment on Comment {
        id,
        content
      }
    `
  }
});
