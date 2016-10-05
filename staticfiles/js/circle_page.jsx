var React = require('react')
var auth = require('./auth')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Router = require('react-router');
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;
var FormGroup = ReactBootstrap.FormGroup;
var FormControl = ReactBootstrap.FormControl;
var ReactDOM = require('react-dom');
var CmsHeader = require('./navbar');
var ControlLabel = ReactBootstrap.ControlLabel;
var Checkbox = ReactBootstrap.Checkbox;
var googleMap = require('./google_map');
var FormControlLabel = ReactBootstrap.ControlLabel;

var Navigation = React.createClass({
    render: function() {
        return (
            <div className="App">
                <CmsHeader />
            </div>
        );
    }
});

var Cirlce = React.createClass({
    render: function() {
        return (
          <div className="restaurant">
            <Row className="text-align-center">
                    // <Col xs={12} md={12}>
                    //         <a><h2 className="restaurantName" onClick={this.MoveToProfile} value={this.props.url}>
                    //           {this.props.name}
                    //         </h2></a>
                    //         <p>Review average: {this.props.avg_score}/10<br/>
                    //         {this.props.children}</p>
                    // </Col>
            </Row>
          </div>
        );
    }

});

var CircleListing = React.createClass({
  loadCirclesFromServer: function() {
        $.ajax({
          method: 'GET',
          url: '/api/circles/',
          dataType: 'json',
          headers: {
                'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
            this.setState({data: data});
            console.log(data);
          }.bind(this),
          error: function(xhr, status, err) {
            console.error("failed to load Circle");
          }.bind(this)
        });
      },
      getInitialState: function() {
        return {
            data:[],
        };
      },
      componentDidMount: function() {
        this.loadCirclesFromServer();
  },
  render() {
    return (
      <div>
        <Navigation/>
        <Row className='sign-up-label text-align-center'>
              <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                   <h1>Circles</h1>
                   <br/>
              </Col>
        </Row>

        <Row className='text-align-center'>
              <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                <h4>Circles you are in</h4>
                   <br/>
                <span>
                    test
                </span>
              </Col>
        </Row>
        <Row>
            <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
            </Col>
        </Row>
    </div>

    )
  }
});



module.exports = CircleListing;