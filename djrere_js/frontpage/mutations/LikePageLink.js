import Relay from 'react-relay';


export default class LikePageLink extends Relay.Mutation {
  static fragments = {
    pageLink: () => Relay.QL`
      fragment on PageLink {
        id
      }
    `
  };

  getMutation() {
    return Relay.QL`
      mutation {
        likePageLink
      }
    `;
  }

  getFatQuery() {
    return Relay.QL`
      fragment on LikePageLink {
        likedPageLink {
          likesNum
        }
      }
    `;
  }

  getVariables() {
    return {
      pageLink: this.props.pageLink.id
    };
  }

  getConfigs() {
    return [
      {
        type: 'FIELDS_CHANGE',
        fieldIDs: {likedPageLink: this.props.pageLink.id}
      }
    ];
  }
}
