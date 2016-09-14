var React = require('react')
var ReactDOM = require('react-dom')
var Router = require('react-router')
var App = require('./app')
var Login = require('./login')
var auth = require('./auth')
var Test = require('./test')
var AddRestaurant = require('./add_restaurant')
var AddPoll = require('./add_poll')
var RestaurantProfile = require('./restaurant_profile')
var FoodieProfile = require('./foodie_profile')
var editProfile = require('./edit_foodie_profile')


function requireAuth(nextState, replace) {
    if (!auth.loggedIn()) {
        replace({
            pathname:'/app/login/',
            state: {nextPathname: '/app/'}
        })
    }
}


ReactDOM.render(
    <Router.Router history={Router.browserHistory}>
        <Router.Route path='/app/add_restaurant/' component={AddRestaurant}/>
        <Router.Route path='/app/add_poll/' component={AddPoll} />
        <Router.Route path='/app/edit_profile/' component={editProfile} />
        <Router.Route path='/app/restaurant/:id' component={RestaurantProfile} />
        <Router.Route path='/app/foodie/:id' component={FoodieProfile} />
        <Router.Route path='/app/login/' component={Login} />
        <Router.Route path='/app/test/' component={Test} />
        <Router.Route name='app' path='/app/' component={App} onEnter={requireAuth} />
    </Router.Router>,
    document.getElementById('app')
)
