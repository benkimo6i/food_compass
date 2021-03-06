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
var restaurantList = require('./restaurantListing')
var pollList = require('./pollListing')
var Poll = require('./poll_detail')
var AddCircle = require('./add_circle')
var CircleProfile = require('./circle_profile')
var Circle_page = require('./circle_page')
var CircleEdit = require('./edit_circle')



function requireAuth(nextState, replace) {
    if (!auth.loggedIn()) {
        replace({
            pathname:'/app/login/',
            state: {nextPathname: '/app/'}
        })
    }
}


ReactDOM.render(
        <Router.Router history={ Router.browserHistory }>
            <Router.Route path='/app/'>
                <Router.Route path='/app/login/' component={Login} />
                <Router.Route onEnter={requireAuth}>
                    <Router.IndexRoute component={App}/>
                    <Router.Route path='/app/polls/' component={pollList} />
                    <Router.Route path='/app/add_restaurant/' component={AddRestaurant} />
                    <Router.Route path='/app/add_poll/' component={AddPoll} />
                    <Router.Route path='/app/edit_profile/' component={editProfile} />
                    <Router.Route path='/app/restaurant/:id' component={RestaurantProfile} />
                    <Router.Route path='/app/foodie/:id' component={FoodieProfile} />
                    <Router.Route path='/app/test/' component={Test} />
                    <Router.Route path='/app/restaurant/' component={restaurantList} />
                    <Router.Route path='/app/polls/' component={pollList} />
                    <Router.Route path='/app/polls/:id' component={Poll} />
                    <Router.Route path='/app/add_circle/' component={AddCircle} />
                    <Router.Route path='/app/circles/' component={Circle_page} />
                    <Router.Route path='/app/circles/:id' component={CircleProfile} />
                    <Router.Route path='/app/edit_circles/:id' component={CircleEdit} />

                </Router.Route>
            </Router.Route>
        </Router.Router>,
    document.getElementById('app')
)
