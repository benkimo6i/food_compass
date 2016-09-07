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
var Router = require('react-router');




var CmsHeader = React.createClass({
    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/app/login/')
    },
    returnHome: function() {
        this.context.router.push('/app/');
    },
    goAddRestaurant: function() {
        this.context.router.push('/app/add_restaurant/');
    },
    goToFoodieProfile: function() {
        var foodie_key = this.state.user.foodie_id;
        this.context.router.push('/app/foodie/'+foodie_key);
    },
    goAddPoll: function() {
        this.context.router.push('/app/add_poll/');
    },
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
    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/app/login/')
    },

    getInitialState: function() {
        return {'user':[]}
    },
    componentDidMount: function() {
        this.loadUserData()
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
                this.setState({user: res})
            }.bind(this)
        })
    },

    render: function() {
                if (this.state.user.is_staff) {
                    const navbarInstance = (
                      <Navbar>
                        <Navbar.Header>
                          <Navbar.Brand>
                            <a onClick={this.returnHome}>Food Compass</a>
                          </Navbar.Brand>
                          <Navbar.Toggle />
                        </Navbar.Header>
                        <Navbar.Collapse>
                          <Nav>
                            <NavItem eventKey={1} onClick={this.returnHome}>Home</NavItem>
                            <NavItem eventKey={2} onClick={this.goAddPoll}>Add Poll</NavItem>
                            <NavItem eventKey={3} onClick={this.goAddRestaurant}>Add Restaurants</NavItem>

                          </Nav>
                          <Nav pullRight>
                            <NavItem eventKey={2} onClick={this.goToFoodieProfile}>{this.state.user.username}</NavItem>
                            <NavItem eventKey={1} href="#" onClick={this.logoutHandler}>Log out</NavItem>
                          </Nav>
                        </Navbar.Collapse>
                      </Navbar>
                    );
                    return navbarInstance;
                } else {
                    const navbarInstance = (
                      <Navbar>
                        <Navbar.Header>
                          <Navbar.Brand>
                            <a href="">Food Compass</a>
                          </Navbar.Brand>
                          <Navbar.Toggle />
                        </Navbar.Header>
                        <Navbar.Collapse>
                        <Nav>
                            <NavItem eventKey={1} onClick={this.returnHome}>Home</NavItem>
                            <NavItem eventKey={2} onClick={this.goAddPoll}>Add Poll</NavItem>

                          </Nav>

                          <Nav pullRight>
                            <NavItem eventKey={2} onClick={this.goToFoodieProfile}>{this.state.user.username}</NavItem>
                            <NavItem eventKey={1} href="#" onClick={this.logoutHandler}>Log out</NavItem>
                          </Nav>
                        </Navbar.Collapse>
                      </Navbar>
                    );
                    return navbarInstance;
                }

    }
});

module.exports = CmsHeader;
