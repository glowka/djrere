import Relay from 'react-relay';

export default class AddCommentMutation extends Relay.Mutation {
  static fragments = {
    frontLink: () => Relay.QL`
      fragment on FrontLink {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`mutation {addComment}`;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on AddComment {
        link {
          id,
          comments
        }
        commentEdge
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'RANGE_ADD',
        parentName: 'link',
        parentID: this.props.frontLink.id,
        connectionName: 'comments',
        edgeName: 'commentEdge',
        rangeBehaviors: {
          '': 'append',
        }
      }
    ];
  }

  getVariables() {
    return {
      linkId: this.props.frontLink.id,
      content: this.props.content
    };
  }
}
