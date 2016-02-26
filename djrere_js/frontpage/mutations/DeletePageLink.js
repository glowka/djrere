import Relay from 'react-relay';


export default class AddPageLinkMutation extends Relay.Mutation {
  static fragments = {
    user: () => Relay.QL`
      fragment on User {
        id
        frontpage {
          id
        }
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
        frontpage {
          allPageLinks
        }
      }
    `;
  }

  getConfigs() {
    return [
      {
        type: 'NODE_DELETE',
        parentName: 'frontpage',
        parentID: this.props.user.frontpage.id,
        connectionName: 'allPageLinks',
        deletedIDFieldName: 'deletedPageLinks'
      }
    ];
  }

  getVariables() {
    return {
      pageLink: this.props.pageLink.id,
      user: this.props.user.id
    };
  }
}
