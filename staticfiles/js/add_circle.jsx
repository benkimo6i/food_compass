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



var CircleForm = React.createClass({
  contextTypes: {
        router: React.PropTypes.object.isRequired
  },
  handleCircleSubmit: function(Circle) {
    $.ajax({
      url: '/api/circles/',
      dataType: 'json',
      type: 'POST',
      data: Circle,
      headers: {
                'Authorization': 'Token ' + localStorage.token
      },
      success: function(data) {
            console.log("circle submitted");
            this.context.router.replace('/app/')
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {name: '', description: '', street:'', city:'', state:''};
  },
  handleNameChange: function(e) {
    this.setState({name: e.target.value});
  },
  handleDescriptionChange: function(e) {
    this.setState({description: e.target.value});
  },
  handleStreetChange: function(e) {
    this.setState({street: e.target.value});
  },
  handleCityChange: function(e) {
    this.setState({city: e.target.value});
  },
  handleStateChange: function(e) {
    this.setState({state: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var name = this.state.name.trim();
    var description = this.state.description.trim();
    var street = this.state.street.trim();
    var city = this.state.city.trim();
    var state = this.state.state.trim();
    if (!name || !description || !street || !city || !state) {
      return;
    }
    this.handleCircleSubmit({name: name, description: description, street:street, city:city, state:state});
  },
  render: function() {
    return (
      <div>
          <Navigation/>
          <Row className='sign-up-label text-align-center'>
                        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                            <h1>Add Circle</h1>
                            <br/>
                        </Col>
                      </Row>
                      <Row className='text-align-center'>
                        <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                          <form className="commentForm" onSubmit={this.handleSubmit}>
                            <FormGroup>
                                <FormControl
                                  type="text"
                                  placeholder="Name"
                                  value={this.state.name}
                                  onChange={this.handleNameChange}
                                />
                                <br/>
                                <FormControl
                                  type="text"
                                  placeholder="Description"
                                  value={this.state.description}
                                  onChange={this.handleDescriptionChange}
                                />
                                <br/>
                                 <FormControl
                                  type="text"
                                  placeholder="street"
                                  value={this.state.street}
                                  onChange={this.handleStreetChange}
                                />
                                <br/>
                                 <FormControl
                                  type="text"
                                  placeholder="City"
                                  value={this.state.city}
                                  onChange={this.handleCityChange}
                                />
                                <br/>
                                 <FormControl
                                  type="text"
                                  placeholder="State"
                                  value={this.state.state}
                                  onChange={this.handleStateChange}
                                />
                                <br/>
                                <Button type="submit">Submit</Button>
                            </FormGroup>
                          </form>
                        </Col>
          </Row>
      </div>
    );
  }
});

module.exports = CircleForm