import Relay from 'react-relay';

export default class AddFrontLinkMutation extends Relay.Mutation {
  static fragments = {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
        id
      }
    `,
    frontLink: () => Relay.QL`
      fragment on FrontLink {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`mutation { deleteFrontLink }`;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on DeleteFrontLink {
        deletedFrontLinks,
        viewer {
          allFrontLinks
        }
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'NODE_DELETE',
        parentName: 'viewer',
        parentID: this.props.viewer.id,
        connectionName: 'allFrontLinks',
        deletedIDFieldName: 'deletedFrontLinks'
      }
    ];
  }

  getVariables() {
    return {
      frontLink: this.props.frontLink.id,
      viewer: this.props.viewer.id
    };
  }
}
