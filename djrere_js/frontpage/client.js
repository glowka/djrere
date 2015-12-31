import ReactDOM from 'react-dom';
import router from './router';
// Initing relay
import './relay';

const mountNode = document.createElement('div');
document.body.appendChild(mountNode);

ReactDOM.render(router, mountNode);
