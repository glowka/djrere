import React from 'react';
import Relay from 'react-relay';

import Blog from './Blog';
import UserQueries from '../queries/UserQueries';

class BlogRoute extends Relay.Route {
  static routeName = 'BlogRoute';
  static queries = UserQueries;
}

export default (
  <Relay.RootContainer
    Component={Blog}
    route={new BlogRoute()}
  />
);
