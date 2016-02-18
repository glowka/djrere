import React, { Component } from 'react';
import Relay from 'react-relay';


class Article extends Component {
  static propTypes = {
    article: React.PropTypes.object.isRequired
  };
  render() {
    return (
      <div>
        <p>{this.props.article.title}</p>
        <p>{this.props.article.content}</p>
      </div>
    );
  }
}


export default Relay.createContainer(Article, {
  fragments: {
    article: () => Relay.QL`
      fragment on ArticleNode {
         id, title, content
      }
    `
  }
});
