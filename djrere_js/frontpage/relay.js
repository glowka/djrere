import Relay from 'react-relay';

const djTemplateContext = window.djTemplateContext || {};

export default Relay.injectNetworkLayer(
  new Relay.DefaultNetworkLayer(djTemplateContext.graphqlApiUrl, {
    // Pass all credential data like cookie...
    credentials: 'same-origin',
    // We do some sensitive operations using this api, so always pass csrf header
    headers: {
      'X-CSRFToken': djTemplateContext.csrftoken || ''
    }
  })
);
