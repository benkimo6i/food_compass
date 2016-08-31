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
var ReactDOM = require('react-dom')

var loginHeader = React.createClass({
    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/app/login/')
    },
    contextTypes: {
        router: React.PropTypes.object.isRequired
    },

    handleSubmit: function(e) {
        e.preventDefault()


        var username = ReactDOM.findDOMNode(this.refs.username).value;
        var pass = ReactDOM.findDOMNode(this.refs.pass).value;
        console.log("submit login");
        console.log(username);
        console.log(pass);

        auth.login(username, pass, (loggedIn) => {
            this.context.router.replace('/app/')
        })
    },
    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/app/login/')
    },

    render: function() {
              return (
                <div>
                    <Navbar>
                        <Navbar.Header>
                          <Navbar.Brand>
                            <a href="#">Food Compass</a>
                          </Navbar.Brand>
                          <Navbar.Toggle />
                        </Navbar.Header>
                        <Navbar.Collapse>

                          <Nav pullRight>
                            <form onSubmit={this.handleSubmit}>
                                <Navbar.Form role="form">
                                    <FormGroup>
                                      <FormControl type="text" placeholder="username" ref="username" />
                                      <FormControl type="password" placeholder="password" ref="pass" />
                                      {' '}
                                      <Button type="submit">Login</Button>
                                    </FormGroup>

                                </Navbar.Form>
                            </form>
                          </Nav>
                        </Navbar.Collapse>
                      </Navbar>
                  </div>
              )
    }
});

module.exports = loginHeader;
