document.getElementById("login").addEventListener("submit", (event) => {
  event.preventDefault();
});

firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    location.replace("home.html");
  }
});

function login() {
  const email = document.getElementById("user").value;
  const password = document.getElementById("pass").value;
  firebase
    .auth()
    .signInWithEmailAndPassword(email, password)
    .catch((error) => {
      document.getElementById("error").innerHTML = error.message;
    });
}

function forgotPass() {
  const email = document.getElementById("email").value;
  firebase
    .auth()
    .sendPasswordResetEmail(email)
    .then(() => {
      alert("Reset link sent to your email id");
    })
    .catch((error) => {
      document.getElementById("error").innerHTML = error.message;
    });
}
