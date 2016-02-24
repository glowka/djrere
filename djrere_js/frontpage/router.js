import { createHashHistory } from 'history';
import React from 'react';

import { Route, IndexRoute } from 'react-router';
import { RelayRouter } from 'react-router-relay';
import App from './components/App';
import LandingPage from './components/LandingPage';
import AboutUs from './components/AboutUs';
import UserQueries from './queries/UserQueries';
import EmptyQueries from './queries/EmptyQueries';

const history = createHashHistory();


export default (
  <RelayRouter history={history}>
    <Route path="/" component={App} queries={EmptyQueries}>
      <IndexRoute component={LandingPage} queries={UserQueries}/>
      <Route path="lp" component={LandingPage} queries={UserQueries}/>
      <Route path="about" component={AboutUs} queries={EmptyQueries}/>
    </Route>
  </RelayRouter>
);
