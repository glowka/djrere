import React from 'react';
import Relay from 'react-relay';

import Blog from './Blog';
import ViewerQueries from '../queries/ViewerQueries';

class BlogRoute extends Relay.Route {
  static routeName = 'BlogRoute';
  static queries = ViewerQueries;
}

export default (
  <Relay.RootContainer
    Component={Blog}
    route={new BlogRoute()}
  />
);
