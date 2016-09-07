var React = require('react')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;
var CmsHeader = require('./navbar');
var FormGroup = ReactBootstrap.FormGroup;
var FormControl = ReactBootstrap.FormControl;

var Navigation = React.createClass({
    render: function() {
        return (
            <div className="App">
                <CmsHeader />
            </div>
        );
    }
});

var FoodieProfile = React.createClass({
  loadFoodieData: function(foodie_id){
        $.ajax({
            method: 'GET',
            url: '/api/foodies/'+String(foodie_id)+'/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                console.log(res);
                this.setState({foodie: res});
                this.setState({username:res.user.username});
                this.setState({foodie_pk:res.id});
            }.bind(this)
        })
  },
  getInitialState: function() {
    return {
        foodie:[],
        user:[],
        username:[],
        foodie_pk:[],
        url_param: this.props.params.id,
    };
  },
  componentDidMount: function() {
    console.log("profile mounting");
    this.loadFoodieData(this.state.url_param);
  },
  render: function() {
    return (
        <div>
          <Navigation/>
          <div className="Profile">
            <Row className="text-align-center">
                <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                           <h1>{this.state.username}</h1>
                </Col>
            </Row>
            <ReviewBox foodie_pk={this.state.foodie_pk} />
          </div>
        </div>
    );
  }
});



var Review = React.createClass({
  render: function() {
    return (
      <div className="Review">
        <h2 className="ReviewAuthor">
          {this.props.subject}
        </h2>
        <h3>score: {this.props.score}</h3>
        <span>{this.props.children}</span>
      </div>
    );
  }
});

var Review = React.createClass({
  render: function() {
    return (
      <div className="Review">
        <h2 className="ReviewAuthor">
          {this.props.subject}
        </h2>
        <span><em>By: {this.props.foodie_name}</em> on {this.props.added_on}</span><br/>
        <span>score: {this.props.score}/10</span>
        <span><p>{this.props.children}</p></span>
      </div>
    );
  }
});

var ReviewBox = React.createClass({
  loadReviewsFromServer: function() {
    var reviews_url = "/api/reviews/?foodie="+String(this.props.foodie_pk);
    if (this.state.sort == "score") {
        reviews_url = reviews_url + "&ordering=score"
    }
    else if (this.state.sort == "added") {
        reviews_url = reviews_url + "&ordering=added"
    }
    $.ajax({
     method: 'GET',
            url: reviews_url,
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(data) {
                console.log(reviews_url);
                this.setState({data: data});
            }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  updateSort: function(event) {
    console.log("sort update");
    if (event.target.value == "score") {
        this.setState({sort: "score"}, function() {
            console.log(this.state.sort);
            this.loadReviewsFromServer();
        })
    }
    else if (event.target.value == "added") {
        this.setState({sort: "added"}, function() {
            console.log(this.state.sort);
            this.loadReviewsFromServer();
        })
    }
  },
  getInitialState: function() {
    return {
        data: [],
        url_param:this.props.restaurantPk,
        limit: 5,
        offset:0,
        sort:[],

    };
  },
  componentDidMount: function() {
    console.log("loading reviews");
    setTimeout(this.loadReviewsFromServer, 500);
  },
  render: function() {
    return (
      <div className="ReviewBox">
        <Row className="text-align-center">
            <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                       <h1>Reviews</h1>
            </Col>
        </Row>
        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                       <span>Sort by: <Button value="score" onClick={this.updateSort}>Score</Button> <Button value="added" onClick={this.updateSort}>Date</Button></span>
        </Col>
        <ReviewList data={this.state.data} />
      </div>
    );
  }
});

var ReviewList = React.createClass({
  render: function() {
    var reviewNodes = this.props.data.map(function(review) {
      return (
        <Review subject={review.subject} key={review.id} url={review.url} score={review.score} foodie_name={review.foodie.user.username} added_on={review.added}>
          {review.comment}
        </Review>
      );
    }, this);
    return (
      <Row>
        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                   {reviewNodes}
        </Col>
      </Row>
    );
  }
});

module.exports = FoodieProfile