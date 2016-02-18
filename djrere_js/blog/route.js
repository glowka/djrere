import Relay from 'react-relay';
import ViewerQueries from './queries/ViewerQueries'


export default class BlogRoute extends Relay.Route {
  static routeName = 'BlogRoute';
  static queries = ViewerQueries;
}
