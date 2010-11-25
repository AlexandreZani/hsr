function onLoginButtonClick() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  api = getHsrApi();
  api.login(username, password, loginCallback);
}

function loginCallback(response, credentials, error, msg) {
  if(credentials != null) {
    var exdate=new Date();
    exdate.setDate(exdate.getDate()+1);
    document.cookie="credentials="+(new XMLSerializer()).serializeToString(credentials)+";expires="+exdate.toUTCString();
  } else {
    document.getElementById("invalid_login").setAttribute("style", "");
  }
}
