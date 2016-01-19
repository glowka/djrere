import Relay from 'react-relay';

export default class AddPageLinkMutation extends Relay.Mutation {
  static fragments = {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
        id
      }
    `,
    pageLink: () => Relay.QL`
      fragment on PageLink {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`mutation { deletePageLink }`;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on DeletePageLink {
        deletedPageLinks,
        viewer {
          allPageLinks
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
        connectionName: 'allPageLinks',
        deletedIDFieldName: 'deletedPageLinks'
      }
    ];
  }

  getVariables() {
    return {
      pageLink: this.props.pageLink.id,
      viewer: this.props.viewer.id
    };
  }
}
