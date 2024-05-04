var valueTemp = firebase.database().ref("Day");
valueTemp.on("value", (snap) => {
  console.log("Day: " + snap.val());
  document.getElementById("day").innerHTML = snap.val() + " days";
});

var valueStage = firebase.database().ref("grown_up");
valueStage.on("value", (snap) => {
  if (snap.val() == 0) {
    console.log("Stage: cây non  ");
    document.getElementById("plant_stage").innerHTML = "Immature";
  } else {
    console.log("Stage: cây non  ");
    document.getElementById("plant_stage").innerHTML = " Mature";
  }
});

var valueTemp = firebase.database().ref("Value").child("temp_air");
valueTemp.on("value", (snap) => {
  console.log("nhiet do: " + snap.val());
  document.getElementById("temperature").innerHTML = snap.val() + " °C";
});

var valueHum = firebase.database().ref("Value").child("hum");
valueHum.on("value", (snap) => {
  console.log("do am: " + snap.val());
  document.getElementById("humidity").innerHTML = snap.val() + " %";
});

var valueHum = firebase.database().ref("Value").child("temp_water");
valueHum.on("value", (snap) => {
  console.log("nhiet do nuoc: " + snap.val());
  document.getElementById("temperature_water").innerHTML = snap.val() + " °C";
});

var valuepH = firebase.database().ref("Value").child("pH");
valuepH.on("value", (snap) => {
  console.log("pH: " + snap.val());
  document.getElementById("pH").innerHTML = snap.val() + " pH";
});

var valueppm = firebase.database().ref("Value").child("ppm");
valueppm.on("value", (snap) => {
  console.log("ppm: " + snap.val());
  document.getElementById("ppm").innerHTML = snap.val() + " ppm";
});

var valueppm = firebase.database().ref("Value").child("lux");
valueppm.on("value", (snap) => {
  console.log("lux: " + snap.val());
  document.getElementById("light_int").innerHTML = snap.val() + " lux";
});