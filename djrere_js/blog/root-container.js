import { createHashHistory } from 'history';
import React from 'react';
import Relay from 'react-relay';

import Blog from './components/Blog';
import BlogRoute from './route'

export default (
  <Relay.RootContainer
    Component={Blog}
    route={new BlogRoute()}
  />
);
