import Blog from './components/Blog';
import Child from './components/Child';
import BlogRoot from './components/BlogRoot';
import UserQueries from './queries/UserQueries';


export default [
  { path: '/blog/',
    component: Blog,
    queries: UserQueries,

    //indexRoute: { component: BlogRoot }
    childRoutes: [
      { path: 'child/', component: Child },
    ]
    //  { path: 'inbox',
    //    component: Inbox,
    //    childRoutes: [
    //      { path: '/messages/:id', component: Message },
    //      { path: 'messages/:id',
    //        onEnter: function (nextState, replace) {
    //          replace('/messages/' + nextState.params.id)
    //        }
    //      }
    //    ]
    //  }
    //]
  }
];


