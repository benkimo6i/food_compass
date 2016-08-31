var React = require('react')
var ReactBootstrap = require('react-bootstrap');
var Grid = ReactBootstrap.Grid;
var Row = ReactBootstrap.Row;
var Col = ReactBootstrap.Col;
var Input = ReactBootstrap.Input;
var Button = ReactBootstrap.Button;

module.exports = React.createClass({
    render: function() {
        return (
            <Grid>
                    <Row>

                        <Col xs={6} md={6}>
                          <Button>Clear</Button>
                        </Col>


                    </Row>
            </Grid>
        )
    }
});


