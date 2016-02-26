import React from 'react';
import ReactDOM from 'react-dom';
import routes from './routes';
import { Router,  browserHistory } from 'react-router';
import { RelayRouter } from 'react-router-relay';

// Pure import only to initialize relay
import './relay';


// Rendering components directly into document.body is discouraged, adding wrapper.
const mountNode = document.createElement('div');
document.body.appendChild(mountNode);
mountNode.id = 'client-root';

ReactDOM.render(
  <RelayRouter history={browserHistory} routes={routes} />,
  mountNode
);
