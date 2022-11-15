$(document).ready(function () {

    $("#Login").click(
        function () {
            document.data.action = "LoginServlet"
            document.data.submit();
        }
    );

    $("#Register").click(
        function () {
            document.data.action = "AutoFillServlet"
            document.data.submit();
        }
    );
});



