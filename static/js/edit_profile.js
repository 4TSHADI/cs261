$( function() {
    $("#edit_profile_form").submit( function() {
        let email = $("#email").val();

        let messageBox = $("#messageBox");
        messageBox.empty();

        // Regex to check if a string contains uppercase, lowercase, special characters & numeric value
        let emailPattern = new RegExp(
            "[A-Za-z0-9\.]+@[A-Za-z0-9\.]+\.[A-Za-z0-9\.]+"
        );
        
        if (!emailPattern.test(email)){
            flash("Please enter a valid email address");
            return false;
        }

        return true;
    });

    function flash(message) {
        let messageBox = $("#messageBox");

        messageBox.append("<div class=\"flashedMessage\">" + message + "</div>");
    }
});