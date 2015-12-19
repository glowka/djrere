import {createHistory, createHashHistory} from 'history';
import React from 'react';
import ReactDOM from 'react-dom';


import Relay from 'react-relay';
import {Router, Route, IndexRoute} from 'react-router';
import {RelayRouter} from 'react-router-relay';
import App from './components/App';
import LandingPage from './components/LandingPage';
import AboutUs from './components/AboutUs';

const history = createHashHistory();


export default (
  <Router history={history}>
    <Route path="/" component={App}>
        <IndexRoute component={LandingPage} />
        <Route path="lp" component={LandingPage} />
        <Route path="about" component={AboutUs} />
    </Route>
  </Router>
)