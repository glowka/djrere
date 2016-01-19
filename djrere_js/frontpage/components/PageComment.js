import React, { Component } from 'react';
import Relay from 'react-relay';
import './PageComment.less';


class PageComment extends Component {
  static propTypes = {
    pageComment: React.PropTypes.object.isRequired,
  };

  render() {
    const { pageComment } = this.props;

    return (
      <div className="PageComment-wrapper">{pageComment.content}</div>
    );
  }
}


export default Relay.createContainer(PageComment, {
  fragments: {
    pageComment: () => Relay.QL`
      fragment on PageComment {
        id,
        content
      }
    `
  }
});
