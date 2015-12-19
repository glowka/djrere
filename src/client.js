import React from 'react';
import ReactDom from 'react-dom';
import App from './App';


const mountNode = document.createElement('div');
document.body.appendChild(mountNode);

ReactDom.render(<App />, mountNode);
