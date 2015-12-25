import Relay from 'react-relay';

console.log(djTemplateContext);
console.log('jjkjkj');
var djTemplateContext = window.djTemplateContext || {};

export default Relay.injectNetworkLayer(
  new Relay.DefaultNetworkLayer('/frontpage/graph-api/', {
    headers: {
      'X-CSRFTOKEN': djTemplateContext.csrftoken || '',
    },
  })
);