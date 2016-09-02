var React = require('react')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;
var Router = require('react-router');

var Choice = React.createClass({
  MoveToProfile: function (event) {
    console.log("move calls");
    console.log(String(this.props.restaurant_id));
    this.props.handleMoveToProfile(String(this.props.restaurant_id));
  },
  getInitialState: function() {
    return {data: '', restaurant:[],};
  },
  componentDidMount: function() {
        this.loadRestaurantFromServer();
  },
  loadRestaurantFromServer: function() {
        var restaurants_url = "/api/restaurants/"+String(this.props.restaurant_id);
        $.ajax({
          method: 'GET',
          url: restaurants_url,
          dataType: 'json',
          headers: {
                'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
            this.setState({data: data});
            this.setState({restaurant: data.restaurant});
            console.log(data);
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
      },
  render: function() {
    return (
      <div className="restaurant text-align-center">
                <Col xs={3} md={3}>
                        <a><h2 className="restaurantName" onClick={this.MoveToProfile} value={this.props.restaurant_id}>
                          {this.state.restaurant.name}
                        </h2></a>
                        <p>Review average: {this.state.data.average_score}/10<br/>
                        {this.state.restaurant.description}</p>
                        <Button>Vote</Button>
                </Col>

      </div>
    );
  }
});


var Poll = React.createClass({
  goToRestaurantProfile: function(restaurantKey) {
        this.context.router.push('/app/restaurant/'+String(restaurantKey));
    },
  contextTypes: {
        router: React.PropTypes.object.isRequired
  },
  render: function() {
    var ChoicesNodes = this.props.choices.map(function(choice) {
      return (
        <Choice restaurant_id={choice} handleMoveToProfile={this.goToRestaurantProfile}>
        </Choice>
      );
    }, this);
    return (
      <div className="Poll">
        <Row className="text-align-center poll-row">
                <Col xs={12} md={12}>
                        <a><h2 className="PollName" value={this.props.url}>
                          {this.props.title}
                        </h2></a>
                        <p>Added on: {this.props.added}<br/>
                        {this.props.children}</p>
                        <Col xs={12} md={12}>
                            {ChoicesNodes}
                        </Col>
                </Col>
        </Row>
      </div>
    );
  }
});

var PollPage= React.createClass({
      loadPollsFromServer: function() {
        console.log("polls page mounted - loading");
        var Polls_url = "/api/polls/";
        $.ajax({
          method: 'GET',
          url: Polls_url,
          dataType: 'json',
          headers: {
                'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
            console.log("polls page mounted - loading success");
            console.log(data);
            this.setState({data: data}, function() {
                console.log(this.state.data);
            });
          }.bind(this),
          error: function(xhr, status, err) {
            console.log("polls page mounted - loading failed");
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
      },
      getInitialState: function() {
        return {data: [],
            sort:[],
            order:[],
        };
      },
      componentDidMount: function() {
        console.log("polls page mounted");
        this.loadPollsFromServer();
      },

    render: function() {
        return (
            <Row className="text-align-center">
                <Col xs={12} md={12}>
                           <h1>Polls</h1>
                           <PollList data={this.state.data} />
                </Col>
            </Row>


        )
    }
});

var PollList = React.createClass({
  render: function() {
    var PollNodes = this.props.data.map(function(poll) {
      return (
        <Poll title={poll.title} choices={poll.Restaurants} added={poll.added}>
          {poll.description}
        </Poll>
      );
    }, this);
    return (
      <div className="PollList">
        {PollNodes}
      </div>
    );
  }
});

module.exports = PollPage;