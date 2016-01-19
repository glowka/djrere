import React from 'react';
import ReactDOM from 'react-dom';
import GraphiQL from 'graphiql';
import graphQLFetcher from './fetcher';

import 'graphiql/graphiql.css';
import './client.less';


// Rendering components directly into document.body is discouraged, adding wrapper.
const mountNode = document.createElement('div');
document.body.appendChild(mountNode);
mountNode.id = 'client-root';

ReactDOM.render(<GraphiQL fetcher={graphQLFetcher} />, mountNode);
