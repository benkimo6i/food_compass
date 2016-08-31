var React = require('react')
var auth = require('./auth')
var CmsHeader = require('./navbar');
var RestaurantPage = require('./restaurant');

var Navigation = React.createClass({
    render: function() {
        return (
            <div className="App">
                <CmsHeader />
            </div>
        );
    }
});

var Restaurant = React.createClass({
    render: function() {
        return (
            <div className="App">
                <RestaurantPage/>
            </div>
        );
    }
});

module.exports = React.createClass({
   getInitialState: function() {
        return {'user':[]}
    },

    componentDidMount: function() {
        this.loadUserData()
    },
            
    contextTypes: {
        router: React.PropTypes.object.isRequired
    },

    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/app/login/')
    },

    loadUserData: function() {
        $.ajax({
            method: 'GET',
            url: '/api/users/i/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                this.setState({user: res})
            }.bind(this)
        })
    },

    render: function() {
        return (

            <div>
                <Navigation/>
                <Restaurant/>
            </div>
        )        
    }
})
