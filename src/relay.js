import Relay from 'react-relay';

console.log(djTemplateContext);
console.log('jjkjkj');
var djTemplateContext = window.djTemplateContext || {};

export default Relay.injectNetworkLayer(
  new Relay.DefaultNetworkLayer('/frontpage/graph-api/', {
    // Pass all credential data like cookie...
    credentials: 'same-origin',
    // We do some sensitive operations using this api, so always pass csrf header
    headers: {
      'X-CSRFToken': djTemplateContext.csrftoken || '',
    },
  })
);