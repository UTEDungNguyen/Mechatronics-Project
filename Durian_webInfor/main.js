var valueDayExport = firebase.database().ref("sample_1").child("date of exportation");
// valueTemp.on("value", (snap) => {
  console.log("Day: " + snap.val());
  document.getElementById("day").innerHTML = snap.val();
// });



var valueOrgin = firebase.database().ref("sample_1").child("orgin");
// valueTemp.on("value", (snap) => {
  console.log("the orgin: " + snap.val());
  document.getElementById("orgin").innerHTML = snap.val() ;
// });

var valueHum = firebase.database().ref("sample_1").child("durian's name");
// valueHum.on("value", (snap) => {
  console.log("durian's name: " + snap.val());
  document.getElementById("name").innerHTML = snap.val() ;
// });

var valueHum = firebase.database().ref("sample_1").child("weight");
// valueHum.on("value", (snap) => {
  console.log("trọng lượng: " + snap.val());
  document.getElementById("weight").innerHTML = snap.val() ;
// });

var valuepH = firebase.database().ref("sample_1").child("type");
// valuepH.on("value", (snap) => {
  console.log("Type: " + snap.val());
  document.getElementById("type").innerHTML = snap.val() ;
// });
