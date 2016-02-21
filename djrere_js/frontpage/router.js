import { createHashHistory } from 'history';
import React from 'react';

import { Route, IndexRoute } from 'react-router';
import { RelayRouter } from 'react-router-relay';
import App from './components/App';
import LandingPage from './components/LandingPage';
import AboutUs from './components/AboutUs';
import ViewerQueries from './queries/ViewerQueries';
import EmptyQueries from './queries/EmptyQueries';

const history = createHashHistory();


export default (
  <RelayRouter history={history}>
    <Route path="/" component={App} queries={EmptyQueries}>
      <IndexRoute component={LandingPage} queries={ViewerQueries}/>
      <Route path="lp" component={LandingPage} queries={ViewerQueries}/>
      <Route path="about" component={AboutUs} queries={EmptyQueries}/>
    </Route>
  </RelayRouter>
);
