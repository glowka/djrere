import React, { Component } from 'react';
import Relay from 'react-relay';
import Footer from './Footer';
import Header from './Header';
import Article from './Article';


class Blog extends Component {
  static propTypes = {
    blog: React.PropTypes.object.isRequired
  };
  render() {
    return (
      <div>
        <Header />
        <ul>
          {this.props.viewer.blog.articles.edges.map(
            ({ node: article }) => <Article article={article} key={article.id} />
          )}
        </ul>
        <Footer />
      </div>
    );
  }
}


export default Relay.createContainer(Blog, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
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
