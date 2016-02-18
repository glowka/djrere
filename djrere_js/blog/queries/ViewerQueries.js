import Relay from 'react-relay';

export default {
  viewer: (Component) => Relay.QL`
      query Viewer {
        viewer { ${Component.getFragment('viewer')} },
      }
    `
};
