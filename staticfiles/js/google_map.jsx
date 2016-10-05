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

var googleMap = React.createClass({

    initTripMap: function () {
        var geocoder = new google.maps.Geocoder();
        var latlng = new google.maps.LatLng(-34.397, 150.644);
        var isDraggable = $(document).width() > 480 ? true : false; // If document (your website) is wider than 480px, isDraggable = true, else isDraggable = false

        var mapOptions = {
              zoom: 6,
              center: latlng,
        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    },
    componentDidMount: function() {
        console.log("creating google map");
        this.initTripMap();
    },
    render: function() {
        return (
            <div className ="mapContainer">
                <div id="map" className="map">
                </div>
            </div>
        );
    }

});

module.exports = googleMap