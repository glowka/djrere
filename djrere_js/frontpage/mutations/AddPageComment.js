import Relay from 'react-relay';

export default class AddPageCommentMutation extends Relay.Mutation {
  static fragments = {
    pageLink: () => Relay.QL`
      fragment on PageLink {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`mutation {addPageComment}`;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on AddPageComment {
        link {
          id,
          pageComments
        }
        pageCommentEdge
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'RANGE_ADD',
        parentName: 'link',
        parentID: this.props.pageLink.id,
        connectionName: 'pageComments',
        edgeName: 'pageCommentEdge',
        rangeBehaviors: {
          '': 'append',
        }
      }
    ];
  }

  getVariables() {
    return {
      linkId: this.props.pageLink.id,
      content: this.props.content
    };
  }
}
