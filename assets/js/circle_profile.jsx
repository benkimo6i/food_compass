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
var ModalTest = require('./modal_test');
var ButtonGroup = ReactBootstrap.ButtonGroup;
var DropdownButton = ReactBootstrap.DropdownButton;
var MenuItem = ReactBootstrap.MenuItem;
var Glyphicon = ReactBootstrap.Glyphicon;

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
  loadUserData: function() {
        $.ajax({
            method: 'GET',
            url: '/api/users/i/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                 console.log("foodie id is "+ String(res.foodie_id));
                 this.setState({foodie_pk: res.foodie_id});
                 this.loadCircleMembershipStatus(res.foodie_id);
            }.bind(this)
        })
  },
  joinCircle: function() {
       var member =  {foodie:this.state.foodie_pk, circle:this.state.data.id}
       console.log(member);
       $.ajax({
          url: '/api/circle_memberships/',
          contentType:'application/json; charset=utf-8',
          dataType: 'json',
          type: 'POST',
          data: JSON.stringify(member),
          headers: {
                    'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
                console.log("member submitted");
          }.bind(this),
          error: function(xhr, status, err) {
            console.log("adding member error");
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
  },
  loadCircleMembershipStatus: function(foodie_id) {
        $.ajax({
          url: '/api/circle_memberships/'+'?circle='+String(this.state.url_param)+'&foodie='+String(foodie_id),
          contentType:'application/json; charset=utf-8',
          dataType: 'json',
          type: 'GET',
          headers: {
                    'Authorization': 'Token ' + localStorage.token
          },
          success: function(data) {
                console.log("checking membership");
                console.log(data);
                this.setState({joined: true});

          }.bind(this),
          error: function(xhr, status, err) {
            console.log("checking membership error");
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
            joined: false,
            url_param: this.props.params.id,
            circle_image: "https://cdn2.iconfinder.com/data/icons/freecns-cumulus/16/519660-164_QuestionMark-256.png",
            data:[],
            foodie: [],
            foodie_pk:[],
        };
      },
      componentDidMount: function() {
        this.loadUserData();
        this.loadCirclesFromServer();
      },


  render() {
    var joinButton;
    if (this.state.joined) {
      joinButton = <Button><Glyphicon glyph="ok" /> Joined</Button>;
    } else {
      joinButton = <Button onClick={this.joinCircle}>Join</Button>;
    }
    return (
      <div>
        <Navigation/>
            <Col xs={12} md={3} className="circleProfileInfo">
                <Row className='sign-up-label text-align-center'>
                           <h1>{this.state.data.name}</h1>
                           <br/>

                           <CircleImage src={this.state.circle_image} responsive/>
                             <br/>
                                   {joinButton}

                            <br/>
                           <br/>
                           <span>
                            {this.state.data.description}
                            </span>
                            <br/>
                            <br/>
                            <br/>
                           <Col xs={12} md={12}>
                               <div className ="mapContainer">
                                   <div id="map" className="map">
                                   </div>
                               </div>
                           </Col>
                </Row>
            </Col>
            <Col xs={12} md={9}>
                <ModalTest/>
            </Col>

    </div>

    )
  }
});



module.exports = CircleProfile;