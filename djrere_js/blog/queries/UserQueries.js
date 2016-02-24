import Relay from 'react-relay';

export default {
  user: (Component) => Relay.QL`
      query User {
        user { ${Component.getFragment('user')} },
      }
    `
};
