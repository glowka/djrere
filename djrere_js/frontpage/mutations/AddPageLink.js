import Relay from 'react-relay';

export default class AddPageLinkMutation extends Relay.Mutation {
  static fragments = {
    viewer: () => Relay.QL`
      fragment on ViewerQuery {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`mutation { addPageLink }`;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on AddPageLink {
        link {
          id,
          href,
          description
        }
        pageLinkEdge,
        viewer {
          allPageLinks
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
        connectionName: 'allPageLinks',
        edgeName: 'pageLinkEdge',
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
