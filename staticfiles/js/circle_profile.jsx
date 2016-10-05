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
var CircleImage = ReactBootstrap.Image;

var Navigation = React.createClass({
    render: function() {
        return (
            <div className="App">
                <CmsHeader />
            </div>
        );
    }
});


var CircleProfile = React.createClass({
  contextTypes: {
        router: React.PropTypes.object.isRequired
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
  initTripMap: function (lat, lng) {
        var geocoder = new google.maps.Geocoder();
        var latlng = new google.maps.LatLng(lat, lng);
        var isDraggable = $(document).width() > 480 ? true : false; // If document (your website) is wider than 480px, isDraggable = true, else isDraggable = false

        var mapOptions = {
              zoom: 15,
              center: latlng,
        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: latlng,
            map: map
        });
  },
  loadCirclesFromServer: function() {
        $.ajax({
          method: 'GET',
          url: '/api/circles/'+this.state.url_param+'/',
          dataType: 'json',
          headers: {
                'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
            this.setState({data: data});
            this.setState({circle_image: data.circleimage_set[0].datafile});
            console.log(data);
            this.initTripMap(parseFloat(data.lat), parseFloat(data.log));
          }.bind(this),
          error: function(xhr, status, err) {
            console.error("failed to load Circle");
          }.bind(this)
        });
      },
      getInitialState: function() {
        return {
            url_param: this.props.params.id,
            circle_image: "https://cdn2.iconfinder.com/data/icons/freecns-cumulus/16/519660-164_QuestionMark-256.png",
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
                   <h1>{this.state.data.name}</h1>
              </Col>

              <Col xs={6} xsOffset={3} sm={6} smOffset={3}>
                   <CircleImage src={this.state.circle_image} circle responsive/>
              </Col>
        </Row>
        <br/>

        <Row className='text-align-center'>
              <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                <span>
                    {this.state.data.description}
                </span>
              </Col>
        </Row>
        <Row>
            <Col xs={8} md={6} xsOffset={2} mdOffset={3}>
                <div className ="mapContainer">
                    <div id="map" className="map">
                    </div>
                </div>
            </Col>
        </Row>
    </div>

    )
  }
});



module.exports = CircleProfile;