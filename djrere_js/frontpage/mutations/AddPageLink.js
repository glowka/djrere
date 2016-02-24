import Relay from 'react-relay';

export default class AddPageLinkMutation extends Relay.Mutation {
  static fragments = {
    user: () => Relay.QL`
      fragment on User {
        id,
        frontpage {
          id
        }
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
        parentID: this.props.user.frontpage.id,
        connectionName: 'allPageLinks',
        edgeName: 'pageLinkEdge',
        rangeBehaviors: {
          '': 'append',
        }
      }
    ];
  }

  getVariables() {
    console.log(this.props.user);
    return {
      href: this.props.href,
      description: this.props.description || '',
      user: this.props.user.id
    };
  }
}
