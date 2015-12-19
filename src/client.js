import React from 'react';
import ReactDOM from 'react-dom';
import router from './router';

const mountNode = document.createElement('div');
document.body.appendChild(mountNode);

ReactDOM.render(router, mountNode
);

