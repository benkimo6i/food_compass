var React = require('react')
var auth = require('./auth')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;
var Navbar =  ReactBootstrap.Navbar;
var Nav = ReactBootstrap.Nav;
var NavItem = ReactBootstrap.NavItem;
var NavDropdown = ReactBootstrap.NavDropdown;
var MenuItem = ReactBootstrap.MenuItem;
var FormGroup = ReactBootstrap.FormGroup;
var FormControl = ReactBootstrap.FormControl;
var ReactDOM = require('react-dom');
var CmsHeader = require('./navbar');
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

var EditCircle = React.createClass({
    handleCircleEdit: function(e) {
        e.preventDefault();
        var name = ReactDOM.findDOMNode(this.refs.name).value;
        var description = ReactDOM.findDOMNode(this.refs.description).value;
        var street = ReactDOM.findDOMNode(this.refs.street).value;
        var city = ReactDOM.findDOMNode(this.refs.city).value;
        var state = ReactDOM.findDOMNode(this.refs.state).value;

        var circleValues = {"name":name,"description":description,"street":street,"city":city,"state":state};
        this.updateCircle(circleValues);

    },
    contextTypes: {
        router: React.PropTypes.object.isRequired
    },
    updateCircle: function(circleValues) {
        console.log("updating circle starting ------");
        console.log(circleValues);
        var continueFlag = false;
        for (var value in circleValues) {
            if (circleValues[value] == "") {
                delete circleValues[value];
            }
            else if (!continueFlag) {
                continueFlag = true;
            }
        };
        console.log(circleValues);
        if (!continueFlag) {
            console.log("No changes");
            return;
        }
        $.ajax({
          url: '/api/circles/'+String(this.state.url_param)+'/',
          contentType:'application/json; charset=utf-8',
          dataType: 'json',
          type: 'PATCH',
          data: JSON.stringify(circleValues),
          headers: {
                    'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
                console.log("circle updated");
                this.context.router.replace('/app/circles/'+String(this.state.url_param)+'/');
          }.bind(this),
          error: function(xhr, status, err) {
            console.log("circle update error");
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    },
    updateProfileImage: function(e) {
        e.preventDefault();
        var imageForm = this.refs.image_form;
        console.log(imageForm);
        var formData = new FormData(imageForm);

        $.ajax({
          url: '/api/circle_image/',
          contentType: false,
          processData: false,
          type: 'POST',
          data : formData,
          headers: {
                    'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
                console.log("circle image updated");
                this.context.router.replace('/app/circles/'+String(this.state.url_param)+'/');
          }.bind(this),
          error: function(xhr, status, err) {
            console.log("circle image error");
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
  },
    componentDidMount: function() {
        this.loadCircleData();
  },
  loadCircleData: function(){
        $.ajax({
            method: 'GET',
            url: '/api/circles/'+String(this.state.url_param)+'/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                console.log("loading circle");
                this.setState({circle: res});
                console.log(this.state.circle);
            }.bind(this)
        })
  },
  getInitialState: function() {
    return {
            circle:[],
            url_param: this.props.params.id,
            };
  },
    render: function() {
              return (
                <div>
                    <Navigation/>
                    <Row className='sign-up-label text-align-center'>
                        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                            <h1>Edit Circle</h1>
                            <br/>
                        </Col>
                    </Row>
                    <Row >
                        <Row className='sign-up-label text-align-center'>
                            <h3>Circle Image</h3>
                        </Row>
                        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                          <form id="image_form" ref="image_form" encType="multipart/form-data" method="POST" onSubmit={this.updateProfileImage}>
                                    <FormGroup>
                                      <FormControlLabel>Profile Image</FormControlLabel>
                                      <FormControl name="image" type="file" placeholder="Profile Image" ref="profile_image"/>
                                      <FormControl className="hidden" name="circle_id" type="text"  value={this.state.url_param}/>
                                      {' '}
                                      <br/>
                                      <Button type="submit">Edit</Button>
                                    </FormGroup>
                          </form>
                        </Col>
                    </Row>
                    <Row >
                        <Row className='sign-up-label text-align-center'>
                            <h3>Circle Information</h3>
                        </Row>
                        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                          <form onSubmit={this.handleCircleEdit}>
                                    <FormGroup>
                                      <FormControlLabel>Circle Name</FormControlLabel>
                                      <FormControl type="text" placeholder={this.state.circle.name} ref="name"/>
                                      <br/>
                                      <FormControlLabel>Description</FormControlLabel>
                                      <FormControl type="text" placeholder={this.state.circle.description} ref="description" />
                                      <br/>
                                      <FormControlLabel>Street</FormControlLabel>
                                      <FormControl type="text" placeholder={this.state.circle.street} ref="street"/>
                                      <br/>
                                      <FormControlLabel>City</FormControlLabel>
                                      <FormControl type="text" placeholder={this.state.circle.city} ref="city"/>
                                      <br/>
                                      <FormControlLabel>State</FormControlLabel>
                                      <FormControl type="text" placeholder={this.state.circle.state} ref="state"/>
                                      <br/>
                                      {' '}
                                      <br/>
                                      <Button type="submit">Edit</Button>
                                    </FormGroup>
                          </form>
                        </Col>
                    </Row>
                  </div>
              )
    }
});

module.exports = EditCircle;
