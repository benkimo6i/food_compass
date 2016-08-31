var React = require('react')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;
var Router = require('react-router');


var Restaurant = React.createClass({
  MoveToProfile: function (event) {
    console.log("move calls");
    console.log(String(this.props.url));
    this.props.handleMoveToProfile(String(this.props.url));
  },
  render: function() {
    return (
      <div className="restaurant">
        <a><h2 className="restaurantName" onClick={this.MoveToProfile} value={this.props.url}>
          {this.props.name}
        </h2></a>
        <span>{this.props.children}</span>
      </div>
    );
  }
});

var RestaurantPage= React.createClass({
      loadRestaurantsFromServer: function() {
        $.ajax({
          method: 'GET',
          url: '/api/restaurants/',
          dataType: 'json',
          headers: {
                'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
            this.setState({data: data});
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
      },
      getInitialState: function() {
        return {data: []};
      },
      componentDidMount: function() {
        this.loadRestaurantsFromServer();
      },

    render: function() {
        return (
            <div className="restaurantPage">
                <h1>Restaurants</h1>
                <RestaurantList data={this.state.data} />
              </div>
        )
    }
});

var RestaurantList = React.createClass({
  goToRestaurantProfile: function(restaurantKey) {
        this.context.router.push('/app/restaurant/'+String(restaurantKey));
    },
  contextTypes: {
        router: React.PropTypes.object.isRequired
  },
  render: function() {
    var restaurantNodes = this.props.data.map(function(restaurant) {
      return (
        <Restaurant name={restaurant.name} key={restaurant.id} url={restaurant.id} handleMoveToProfile={this.goToRestaurantProfile}>
          {restaurant.description}
        </Restaurant>
      );
    }, this);
    return (
      <div className="restaurantList">
        {restaurantNodes}
      </div>
    );
  }
});

module.exports = RestaurantPage