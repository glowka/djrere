import fetch from 'isomorphic-fetch';

import 'graphiql/graphiql.css';

const djTemplateContext = window.djTemplateContext || {};

export default function graphQLFetcher(graphQLParams) {
  return fetch(djTemplateContext.graphqlApiUrl, {
    // Pass all credential data like cookie...
    credentials: 'same-origin',
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': djTemplateContext.csrftoken || '',
    },
    body: JSON.stringify(graphQLParams),
  }).then(response => response.json());
}
