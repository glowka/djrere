import {createHistory, createHashHistory} from 'history';
import React from 'react';
import ReactDOM from 'react-dom';


import Relay from 'react-relay';
import {Router, Route, IndexRoute} from 'react-router';
import {RelayRouter} from 'react-router-relay';
import App from './components/App';
import LandingPage from './components/LandingPage';
import AboutUs from './components/AboutUs';
import AllFrontLinksQueries from './queries/AllFrontLinksQueries'

const history = createHashHistory();


export default (
  <RelayRouter history={history}>
    <Route path="/" component={App}>
      <IndexRoute component={LandingPage} queries={AllFrontLinksQueries} />
      <Route path="lp" component={LandingPage} queries={AllFrontLinksQueries} />
      <Route path="about" component={AboutUs} />
    </Route>
  </RelayRouter>
);
