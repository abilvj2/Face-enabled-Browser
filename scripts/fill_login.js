function fillLogin(username, password) {
    var idEmail = ['email', 'identifierId'];
    for (var i in idEmail) {
        var email_input = document.getElementById(idEmail[i]);
        if (email_input) {
            email_input.value = username;
        }
    }

    var idPassword = ['pass', 'password'];
    for (var i in idPassword) {
        var pass_input = document.getElementById(idPassword[i]);
        if (pass_input) {
            pass_input.value = password;
        }
    }
}
