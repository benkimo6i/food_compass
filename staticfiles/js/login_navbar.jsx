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


var CmsHeader = React.createClass({
    contextTypes: {
        router: React.PropTypes.object.isRequired
    },

    handleSubmit: function(e) {
        e.preventDefault()

        var username = this.refs.username.value
        var pass = this.refs.pass.value

        auth.login(username, pass, (loggedIn) => {
            this.context.router.replace('/app/')
        })
    },

    render: function() {
                const navbarInstance = (
                  <Navbar>
                    <Navbar.Header>
                      <Navbar.Brand>
                        <a href="#">React-Bootstrap</a>
                      </Navbar.Brand>
                      <Navbar.Toggle />
                    </Navbar.Header>
                    <Navbar.Collapse>
                      <Nav>
                        <NavItem eventKey={1} href="#">Link</NavItem>
                        <NavItem eventKey={2} href="#">Link</NavItem>
                        <NavDropdown eventKey={3} title="Dropdown" id="basic-nav-dropdown">
                          <MenuItem eventKey={3.1}>Action</MenuItem>
                          <MenuItem eventKey={3.2}>Another action</MenuItem>
                          <MenuItem eventKey={3.3}>Something else here</MenuItem>
                          <MenuItem divider />
                          <MenuItem eventKey={3.3}>Separated link</MenuItem>
                        </NavDropdown>
                      </Nav>
                      <Nav pullRight>
                            <NavItem eventKey={1}><form onSubmit={this.handleSubmit}>
                            <input type="text" placeholder="username" ref="username"/>
                            <input type="password" placeholder="password" ref="pass"/>
                            <input type="submit"/>
                        </form></NavItem>


                      </Nav>
                    </Navbar.Collapse>
                  </Navbar>
                );
              return navbarInstance;
    }
});

module.exports = CmsHeader;
