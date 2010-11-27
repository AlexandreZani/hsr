function onLoginButtonClick() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var api = getHsrApi();
  api.login(username, password, loginCallback);
}

function loginCallback(response, credentials, error, msg) {
  if(credentials != null) {
    if(window.location.pathname == "/static/login.html")
      window.location = "/static/main.html";

    window.location.reload();
  } else {
    document.getElementById("invalid_login").setAttribute("style", "");
  }
}
