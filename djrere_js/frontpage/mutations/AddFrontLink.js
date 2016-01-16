import Relay from 'react-relay';

export default class AddFrontLinkMutation extends Relay.Mutation {
  static fragments = {};

  getMutation() {
    return Relay.QL`mutation {addFrontLink}`;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on AddFrontLink {
        link {
          id,
          href,
          description
        }
        frontLinkEdge,
        allFrontLinks
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'RANGE_ADD',
        parentName: null,
        parentID: null,
        connectionName: 'allFrontLinks',
        edgeName: 'frontLinkEdge',
        rangeBehaviors: {
          '': 'append',
        }
      }
    ];
  }

  getVariables() {
    return {
      href: this.props.href,
      description: this.props.description || ''
    };
  }
}
