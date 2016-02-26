import Relay from 'react-relay';

export default class AddPageLinkMutation extends Relay.Mutation {
  static fragments = {
    user: () => Relay.QL`
      fragment on User {
        id,
      }
    `,
    frontpage: () => Relay.QL`
      fragment on Frontpage {
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
        frontpage {
          allPageLinks
        }
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'RANGE_ADD',
        parentName: 'frontpage',
        parentID: this.props.frontpage.id,
        connectionName: 'allPageLinks',
        edgeName: 'pageLinkEdge',
        rangeBehaviors: {
          '': 'append'
        }
      }
    ];
  }

  getVariables() {
    return {
      href: this.props.href,
      description: this.props.description || '',
      user: this.props.user.id
    };
  }
}
