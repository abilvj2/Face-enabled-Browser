function fillRegister(first_name, last_name, email, mobile) {
    var idEmail = ['email', 'identifierId', 'u_0_o'];
    for (var i in idEmail) {
        var email_input = document.getElementById(idEmail[i]);
        if (email_input) {
            email_input.value = email;
        }
    }

    var idFname = ['firstName', 'firstname', 'fname', 'u_0_j', 'usernamereg-firstName'];
    for (var i in idFname) {
        var fname_input = document.getElementById(idFname[i]);
        if (fname_input) {
            fname_input.value = first_name;
        }
    }

    var idLname = ['lastName', 'lastname', 'lname', 'u_0_l', 'usernamereg-lastName'];
    for (var i in idLname) {
        var lname_input = document.getElementById(idLname[i]);
        if (lname_input) {
            lname_input.value = last_name;
        }
    }

    var idMobile = ['mobile', 'phone', 'usernamereg-phone'];
    for (var i in idMobile) {
        var mobile_input = document.getElementById(idMobile[i]);
        if (mobile_input) {
            mobile_input.value = mobile;
        }
    }
}
