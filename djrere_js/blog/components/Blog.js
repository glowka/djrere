import React, { Component } from 'react';
import Relay from 'react-relay';
import Footer from './Footer';
import Header from './Header';
import Article from './Article';


class Blog extends Component {
  static propTypes = {
    user: React.PropTypes.object.isRequired
  };

  render() {
    return (
      <div>
        <Header />
        <ul>
          {this.props.user.blog.articles.edges.map(
            ({ node: article }) => <Article article={article} key={"article" + article.id} />
          )}
          {this.props.children}
        </ul>
        <Footer />
      </div>
    );
  }
}


export default Relay.createContainer(Blog, {
  fragments: {
    user: () => Relay.QL`
      fragment on User {
        blog {
          articles(first: 100) {
            edges {
              node {
                ${Article.getFragment('article')}
              }
            }
          }
        }
      }
    `
  }
});
