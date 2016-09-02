module.exports = {
    login: function(username, pass, cb) {
        if (localStorage.token) {
            if (cb) cb(true)
            return
        }
        this.getToken(username, pass, (res) => {
            if (res.authenticated) {
                localStorage.token = res.token
                if (cb) cb(true)
            } else {
                if (cb) cb(false)
            }
        })
    },        
    
    logout: function() {
        delete localStorage.token
    },

    loggedIn: function() {
        return !!localStorage.token
    },

    getToken: function(username, pass, cb) {
        $.ajax({
            type: 'POST',
            url: '/api/obtain-auth-token/',
            data: {
                username: username.toLowerCase(),
                password: pass
            },
            success: function(res){
                cb({
                    authenticated: true,
                    token: res.token
                })
            }
        })
    },

    signUp: function(username, email, pass, confirm_pass, cb) {
        if (pass ===confirm_pass) {
            var context = this;
            $.ajax({
                type: 'POST',
                url: '/api/users/',
                data: {
                    username: username,
                    email:email,
                    password: pass,
                    confirm_pass: confirm_pass,
                },
                success: function(res){
                     context.login(username, pass, cb)
                }
            })
        }
    },
}
