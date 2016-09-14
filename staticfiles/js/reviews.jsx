var React = require('react')
var auth = require('./auth')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;
var FormGroup = ReactBootstrap.FormGroup;
var FormControl = ReactBootstrap.FormControl;
var ReactDOM = require('react-dom');
var CmsHeader = require('./navbar');
var RestaurantPage = require('./restaurant');

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

var ReviewBox = React.createClass({
  loadReviewsFromServer: function() {
    $.ajax({
     method: 'GET',
            url: '/api/reviews/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(data) {
                this.setState({data: data})
            }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleReviewSubmit: function(Review) {
    var Reviews = this.state.data;
    // Optimistically set an id on the new Review. It will be replaced by an
    // id generated by the server. In a production application you would likely
    // not use Date.now() for this and would have a more robust system in place.
    Review.id = Date.now();
    var newReviews = Reviews.concat([Review]);
    this.setState({data: newReviews});
    $.ajax({
      method: 'POST',
      url: '/api/reviews/',
      dataType: 'json',
      data: Review,
      headers: {
            'Authorization': 'Token ' + localStorage.token
      },
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        this.setState({data: Reviews});
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: [], url_param:this.props.params.id};
  },
  componentDidMount: function() {
    console.log("review starts");
    this.loadReviewsFromServer();
  },
  render: function() {
    return (
      <div className="ReviewBox">
        <h1>Reviews</h1>
        <ReviewList data={this.state.data} />
        <ReviewForm onReviewSubmit={this.handleReviewSubmit} />
      </div>
    );
  }
});

var ReviewList = React.createClass({
  render: function() {
    var ReviewNodes = this.props.data.map(function(Review) {
      return (
        <Review subject={Review.subject} key={Review.id} score={Review.score}>
          {Review.comment}
        </Review>
      );
    });
    return (
      <div className="ReviewList">
        {ReviewNodes}
      </div>
    );
  }
});

var ReviewForm = React.createClass({
  getInitialState: function() {
    return {subject:'', restaurant_id: this.props.params.id, wouldGo:'',score:'', comment: ''};
  },
  handleSubjectChange: function(e) {
    this.setState({subject: e.target.value});
  },
  handlewouldGoChange: function(e) {
    if (e.checked) {
        this.setState({wouldGo: true});
    } else {
        this.setState({wouldGo: false});
    }
  },
  handleScoreChange: function(e) {
    this.setState({score: e.target.value});
  },
  handleCommentChange: function(e) {
    this.setState({comment: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var subject = this.state.subject.trim();
    var score = this.state.score;
    var restaurant_id = this.state.restaurant_id;
    var wouldGo = this.state.wouldGo;
    var comment = this.state.comment.trim();
    if (!subject || !score || !restaurant_id || !wouldGo || !comment) {
      return;
    }
    this.props.onReviewSubmit({subject: subject, score: score, restaurant_id:restaurant_id,wouldGo:true, comment:comment});
    this.setState({subject: '', score: '',wouldGo:'', comment:''});
  },
  render: function() {
    return (
      <form className="commentForm" onSubmit={this.handleSubmit}>
                            <FormGroup>
                                <FormControl
                                  type="text"
                                  placeholder="Subject"
                                  value={this.state.subject}
                                  onChange={this.handleSubjectChange}
                                />
                                <br/>
                                <FormControl
                                 type="number"
                                  placeholder="score"
                                  value={this.state.score}
                                  onChange={this.handleScoreChange}
                                />
                                <br/>
                                 <FormControl
                                   type="text"
                                      placeholder="comment"
                                      value = {this.state.comment}
                                      onChange={this.handleCommentChange}
                                />
                                <br/>
                                 <FormControl
                                  onClick={this.handlewouldGoChange(this)} type="checkbox" name="wouldGo"
                                  value={this.state.wouldGo}
                                />

                                <br/>
                                <Button type="submit">Submit</Button>
                            </FormGroup>
                          </form>
    );
  }
});

module.exports = ReviewBox;