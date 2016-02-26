import React, { Component } from 'react';
import Relay from 'react-relay';
import Footer from './Footer';
import Header from './Header';
import Article from './Article';

import { fixObjKey } from '../../utils/relay-fixes';


class Blog extends Component {
  static propTypes = {
    user: React.PropTypes.object.isRequired
  };

  fixRelayProps(props) {
    // Looks like relay is buggy here, fixing by setting proper key
    fixObjKey(props.user.blog, 'articles')
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
        <Header />
        <ul>
          {this.props.user.blog.articles.edges.map(
            ({ node: article }) => <Article article={article} key={article.id} />
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
