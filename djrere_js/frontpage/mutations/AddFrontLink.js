import Relay from 'react-relay';

export default class AddFrontLinkMutation extends Relay.Mutation {
  static fragments = {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`mutation { addFrontLink }`;
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
        viewer {
          allFrontLinks
        }
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'RANGE_ADD',
        parentName: 'viewer',
        parentID: this.props.viewer.id,
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
      description: this.props.description || '',
      viewer: this.props.viewer.id
    };
  }
}
