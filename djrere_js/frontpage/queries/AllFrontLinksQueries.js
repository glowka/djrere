import Relay from 'react-relay';

export default {
  allFrontLinks: () => Relay.QL`query { allFrontLinks }`
};
