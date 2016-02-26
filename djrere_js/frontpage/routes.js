import App from './components/App';
import LandingPage from './components/LandingPage';
import AboutUs from './components/AboutUs';
import UserQueries from './queries/UserQueries';
import EmptyQueries from './queries/EmptyQueries';


export default [
  {
    path: '/',
    childRoutes: [
      {
        path: "/frontpage/", component: App, queries: EmptyQueries,
        childRoutes: [
          {path: 'lp', component: LandingPage, queries: UserQueries},
          {path: 'about', component: AboutUs, queries: EmptyQueries}
        ],
        indexRoute: {component: LandingPage, queries: UserQueries}
      }
    ]
  }
]

