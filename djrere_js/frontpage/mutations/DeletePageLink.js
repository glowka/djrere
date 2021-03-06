import Relay from 'react-relay';


export default class DeletePageLink extends Relay.Mutation {
  static fragments = {
    user: () => Relay.QL`
      fragment on User {
        id
      }
    `,
    frontpage: () => Relay.QL`
      fragment on Frontpage {
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
        frontpage {
          allPageLinks
        }
      }
    `;
  }

  getConfigs() {
    console.log(this.props.pageLink);
    return [
      {
        type: 'NODE_DELETE',
        parentName: 'frontpage',
        parentID: this.props.frontpage.id,
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
