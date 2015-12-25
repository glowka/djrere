import React from 'react';
import ReactDOM from 'react-dom';
import router from './router';
import Relay from './relay';

const mountNode = document.createElement('div');
document.body.appendChild(mountNode);

ReactDOM.render(router, mountNode
);

