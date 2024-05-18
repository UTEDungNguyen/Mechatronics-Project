// check User and logout
firebase.auth().onAuthStateChanged((user) => {
  if (!user) {
    location.replace("index.html");
  } else {
    document.getElementById("user").innerHTML = "Hello, " + user.email;
  }
});

function logout() {
  firebase.auth().signOut();
}

// display value from Firebase

// display value from Firebase
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

//-------------------------MANUAL CONTROL------------------------------

// update value
var valueled = firebase.database().ref("Control").child("led");
valueled.on("value", (snap) => {
  console.log("led: " + snap.val());
  document.getElementById("brightness_manual_slider").value = snap.val();
  document.getElementById("brightness_manual_Value").textContent =
    snap.val() + " %";
});

var valueled = firebase.database().ref("Control").child("ph");
valueled.on("value", (snap) => {
  console.log("ph: " + snap.val());
  document.getElementById("ph_manual_slider").value = snap.val();
  document.getElementById("ph_manual_Value").textContent = snap.val() + " pH";
});

var valueled = firebase.database().ref("Control").child("ppm");
valueled.on("value", (snap) => {
  console.log("led: " + snap.val());
  document.getElementById("ppm_manual_slider").value = snap.val();
  document.getElementById("ppm_manual_Value").textContent = snap.val() + " ppm";
});

//update value after adjust
function change_brightness_manual() {
  var brightnessValue = document.getElementById(
    "brightness_manual_slider"
  ).value;
  document.getElementById("brightness_manual_Value").textContent =
    brightnessValue + " %";
}

function change_ph_manual() {
  var phValue = document.getElementById("ph_manual_slider").value;
  document.getElementById("ph_manual_Value").textContent = phValue + " pH";
}

function change_ppm_manual() {
  var ppmValue = document.getElementById("ppm_manual_slider").value;
  document.getElementById("ppm_manual_Value").textContent = ppmValue + " ppm";
}

// Update config manual value to firebase
function WriteManualToFirebase(brightnessValue, phValue, ppmValue) {
  firebase.database().ref("Control").set({
    led: brightnessValue,
    ph: phValue,
    ppm: ppmValue,
  });
}

function config_manual_clicked() {
  var brightnessValue = document.getElementById(
    "brightness_manual_slider"
  ).value;
  var phValue = document.getElementById("ph_manual_slider").value;
  var ppmValue = document.getElementById("ppm_manual_slider").value;
  WriteManualToFirebase(brightnessValue, phValue, ppmValue);
  alert("Update Successfully");
}

// -----------------ADJUST MODE----------------------
var valueled = firebase.database().ref("Check_mode");
valueled.on("value", (snap) => {
  console.log("mode: " + snap.val());
  if (snap.val() == 1) {
    document.getElementById("toggleSwitch").checked = true;
  } else document.getElementById("toggleSwitch").checked = false;
});

function toggleMode() {
  var toggleSwitch = document.getElementById("toggleSwitch");
  var btn = document.querySelector(".btn");
  // Kiểm tra trạng thái hiện tại của toggleSwitch
  if (toggleSwitch.checked) {
    firebase.database().ref("Check_mode").set(1);
    alert("Turn on auto control mode!!!");
    btn.setAttribute("disabled", true);
  } else {
    firebase.database().ref("Check_mode").set(0);
    alert("Turn off auto control mode!!!");
    btn.removeAttribute("disabled");
  }
}

// Update config value to firebase

// function WriteConfigToFirebase(config_ph,config_ppm){
//     firebase.database().ref('Config').set({
//         pH: config_ph,
//         ppm: config_ppm
//     });
// }

// function config_clicked() {
//     var pH = document.getElementById("config_ph").value;
//     var ppm = document.getElementById("config_ppm").value;
//     WriteConfigToFirebase(pH,ppm);
//     // alert("h3llo");
// }

//-------------------------CONFIG AUTOMATION------------------------------
//Update days from fb
// var valueled = firebase.database().ref("Day");
// valueled.on("value", (snap) => {
//   document.getElementById("day_auto").value = snap.val();
// });

//Update time auto detect update from fb
var value_hour_detect_auto = firebase
  .database()
  .ref("Timer_auto_detect")
  .child("hour");
value_hour_detect_auto.on("value", (snap) => {
  document.getElementById("hour_detect_auto").value = snap.val();
});

var value_min_detect_auto = firebase
  .database()
  .ref("Timer_auto_detect")
  .child("min");
value_min_detect_auto.on("value", (snap) => {
  document.getElementById("min_detect_auto").value = snap.val();
});

//Update time auto lighting update from fb
var value_hour_lighting_auto = firebase
  .database()
  .ref("Timer_lighting")
  .child("hour");
value_hour_lighting_auto.on("value", (snap) => {
  document.getElementById("hour_lighting_auto").value = snap.val();
});

var value_min_lighting_auto = firebase
  .database()
  .ref("Timer_lighting")
  .child("min");
value_min_lighting_auto.on("value", (snap) => {
  document.getElementById("min_lighting_auto").value = snap.val();
});

//----------------auto1---------------

//update  value auto1 from FB
var valueled = firebase.database().ref("Auto_1").child("led");
valueled.on("value", (snap) => {
  document.getElementById("brightness_auto_1_slider").value = snap.val();
  document.getElementById("brightness_auto_1_Value").textContent =
    snap.val() + " %";
});

var valueled = firebase.database().ref("Auto_1").child("ph");
valueled.on("value", (snap) => {
  document.getElementById("ph_auto_1_slider").value = snap.val();
  document.getElementById("ph_auto_1_Value").textContent = snap.val() + " pH";
});

var valueled = firebase.database().ref("Auto_1").child("ppm");
valueled.on("value", (snap) => {
  document.getElementById("ppm_auto_1_slider").value = snap.val();
  document.getElementById("ppm_auto_1_Value").textContent = snap.val() + " ppm";
});

var valueled = firebase.database().ref("Auto_1").child("time");
valueled.on("value", (snap) => {
  document.getElementById("time_auto_1_slider").value = snap.val();
  document.getElementById("time_auto_1_Value").textContent =
    snap.val() + " hour/day";
});

//update value Auto1 after adjust
function change_brightness_auto_1() {
  var brightnessValue = document.getElementById(
    "brightness_auto_1_slider"
  ).value;
  document.getElementById("brightness_auto_1_Value").textContent =
    brightnessValue + " %";
}

function change_time_auto_1() {
  var ppmValue = document.getElementById("time_auto_1_slider").value;
  document.getElementById("time_auto_1_Value").textContent =
    ppmValue + " hour/day";
}

function change_ph_auto_1() {
  var phValue = document.getElementById("ph_auto_1_slider").value;
  document.getElementById("ph_auto_1_Value").textContent = phValue + " pH";
}

function change_ppm_auto_1() {
  var ppmValue = document.getElementById("ppm_auto_1_slider").value;
  document.getElementById("ppm_auto_1_Value").textContent = ppmValue + " ppm";
}

//----------------auto2---------------

//update  value Auto2 from FB
var valueled = firebase.database().ref("Auto_2").child("led");
valueled.on("value", (snap) => {
  console.log("led: " + snap.val());
  document.getElementById("brightness_auto_2_slider").value = snap.val();
  document.getElementById("brightness_auto_2_Value").textContent =
    snap.val() + " %";
});

var valueled = firebase.database().ref("Auto_2").child("ph");
valueled.on("value", (snap) => {
  console.log("ph: " + snap.val());
  document.getElementById("ph_auto_2_slider").value = snap.val();
  document.getElementById("ph_auto_2_Value").textContent = snap.val() + " pH";
});

var valueled = firebase.database().ref("Auto_2").child("ppm");
valueled.on("value", (snap) => {
  console.log("led: " + snap.val());
  document.getElementById("ppm_auto_2_slider").value = snap.val();
  document.getElementById("ppm_auto_2_Value").textContent = snap.val() + " ppm";
});

var valueled = firebase.database().ref("Auto_2").child("time");
valueled.on("value", (snap) => {
  console.log("led: " + snap.val());
  document.getElementById("time_auto_2_slider").value = snap.val();
  document.getElementById("time_auto_2_Value").textContent =
    snap.val() + " hour/day";
});

//update value Auto2 after adjust
function change_brightness_auto_2() {
  var brightnessValue = document.getElementById(
    "brightness_auto_2_slider"
  ).value;
  document.getElementById("brightness_auto_2_Value").textContent =
    brightnessValue + " %";
}

function change_time_auto_2() {
  var ppmValue = document.getElementById("time_auto_2_slider").value;
  document.getElementById("time_auto_2_Value").textContent =
    ppmValue + " hour/day    ";
}

function change_ph_auto_2() {
  var phValue = document.getElementById("ph_auto_2_slider").value;
  document.getElementById("ph_auto_2_Value").textContent = phValue + " pH";
}

function change_ppm_auto_2() {
  var ppmValue = document.getElementById("ppm_auto_2_slider").value;
  document.getElementById("ppm_auto_2_Value").textContent = ppmValue + " ppm";
}

// -----UPDATE CONFIG VALUE TO FB-----
function WriteAuto1ToFirebase(brightnessValue, timeValue, phValue, ppmValue) {
  firebase.database().ref("Auto_1").set({
    led: brightnessValue,
    ph: phValue,
    ppm: ppmValue,
    time: timeValue,
  });
}

function WriteAuto2ToFirebase(brightnessValue, timeValue, phValue, ppmValue) {
  firebase.database().ref("Auto_2").set({
    led: brightnessValue,
    ph: phValue,
    ppm: ppmValue,
    time: timeValue,
  });
}

function WriteTimerDetectToFirebase(hour, min) {
  firebase.database().ref("Timer_auto_detect").set({
    hour: hour,
    min: min,
  });
}

function WriteTimerLightingToFirebase(hour, min) {
  firebase.database().ref("Timer_lighting").set({
    hour: hour,
    min: min,
  });
}

function config_auto_clicked() {
  // var day = document.getElementById("day_auto").value;

  var hour_detect_auto = document.getElementById("hour_detect_auto").value;
  var min_detect_auto = document.getElementById("min_detect_auto").value;

  var hour_lighting = document.getElementById("hour_lighting_auto").value;
  var min_lighting = document.getElementById("min_lighting_auto").value;

  var brightnessValue1 = document.getElementById(
    "brightness_auto_1_slider"
  ).value;
  var timeValue1 = document.getElementById("time_auto_1_slider").value;
  var phValue1 = document.getElementById("ph_auto_1_slider").value;
  var ppmValue1 = document.getElementById("ppm_auto_1_slider").value;

  var brightnessValue2 = document.getElementById(
    "brightness_auto_2_slider"
  ).value;
  var timeValue2 = document.getElementById("time_auto_2_slider").value;
  var phValue2 = document.getElementById("ph_auto_2_slider").value;
  var ppmValue2 = document.getElementById("ppm_auto_2_slider").value;

  // firebase.database().ref("Day").set(day);
  WriteAuto1ToFirebase(brightnessValue1, timeValue1, phValue1, ppmValue1);
  WriteAuto2ToFirebase(brightnessValue2, timeValue2, phValue2, ppmValue2);
  WriteTimerDetectToFirebase(hour_detect_auto, min_detect_auto);
  WriteTimerLightingToFirebase(hour_lighting, min_lighting);
  alert("Update Successfully");
}

//-------------------------POSITION CONTROL------------------------------
// update position to Firebase
function WritePositionToFirebase(position) {
  firebase.database().ref("Position").set({
    pos: position,
  });
}

function pos1_clicked() {
  WritePositionToFirebase(1);
}
function pos2_clicked() {
  WritePositionToFirebase(2);
}
function pos3_clicked() {
  WritePositionToFirebase(3);
}
function pos4_clicked() {
  WritePositionToFirebase(4);
}
function pos5_clicked() {
  WritePositionToFirebase(5);
}
function pos6_clicked() {
  WritePositionToFirebase(6);
}
function pos7_clicked() {
  WritePositionToFirebase(7);
}
function pos8_clicked() {
  WritePositionToFirebase(8);
}
function pos9_clicked() {
  WritePositionToFirebase(9);
}
function pos10_clicked() {
  WritePositionToFirebase(10);
}
function pos11_clicked() {
  WritePositionToFirebase(11);
}
function pos12_clicked() {
  WritePositionToFirebase(12);
}
function pos13_clicked() {
  WritePositionToFirebase(13);
}
function pos14_clicked() {
  WritePositionToFirebase(14);
}
function pos15_clicked() {
  WritePositionToFirebase(15);
}
function pos16_clicked() {
  WritePositionToFirebase(16);
}
function pos17_clicked() {
  WritePositionToFirebase(17);
}
function pos18_clicked() {
  WritePositionToFirebase(18);
}
function pos19_clicked() {
  WritePositionToFirebase(19);
}
function posHome_clicked() {
  WritePositionToFirebase(0);
}

// kiểm tra  state plant và hiển thị ảnh lên warning và hiển thị viền đỏ ở button
// Khởi tạo kết nối Firebase
var storage = firebase.storage();
var statePlantRef = firebase.database().ref("state_plant");
var containerElement = document.querySelector(".container");
// Lấy dữ liệu từ Firebase Realtime Database
statePlantRef
  .once("value")
  .then(function (snapshot) {
    var state_plant = snapshot.val();

    // Kiểm tra và hiển thị các cây có giá trị "abnormal"
    for (var key in state_plant) {
      console.log(key);
      if (state_plant.hasOwnProperty(key)) {
        var plantState = state_plant[key];

        if (plantState === "abnormal") {
          // Lấy đường dẫn đến ảnh trong Firebase Storage
          var imagePath = key + ".jpg";
          // Lấy tham chiếu đến ảnh trong Firebase Storage
          var imageRef = storage.ref().child(imagePath);

          // Lấy URL tải xuống ảnh
          // imageRef.getDownloadURL().then(function(url) {
          //     // Hiển thị ảnh
          //     var img = document.createElement('img');
          //     img.src = url;
          //     document.body.appendChild(img);

          //     // Lấy tên cây
          //     console.log(key);
          //     var plantName = key.replace('plant','');

          //     var nameElement = document.createElement('p');
          //     nameElement.textContent = 'Tên cây: ' + plantName;
          //     console.log(plantName);
          //     document.body.appendChild(nameElement);
          // }).catch(function(error) {
          //     console.log(error);
          // });
          (function (key) {
            // Lấy URL tải xuống ảnh
            imageRef
              .getDownloadURL()
              .then(function (url) {
                var articleElement = document.createElement("div");
                articleElement.classList.add("card");
                // Hiển thị ảnh
                var plantName = key.replace("plant", "");
                const template = `
                <img
                  class="card__background"
                  src="${url}"
                  alt="image"
                />
                <div class="card__content | flow">
                  <div class="card__content--container | flow">
                    <h2 class="card__title">Plant ${plantName}</h2>
                  </div>
                </div>
                `;
                articleElement.innerHTML = template;
                if (containerElement)
                  containerElement.appendChild(articleElement);
                else document.body.appendChild(articleElement);
                var button_id = "button_" + plantName;
                console.log(button_id);
                // Kiểm tra ID của button và đặt viền đỏ nếu ID khớp với key

                document.getElementById(button_id).style.border =
                  "2px solid red"; // Thêm viền đỏ cho button
              })
              .catch(function (error) {
                console.log(error);
              });
          })(key);
        }
      }
    }
  })
  .catch(function (error) {
    console.log(error);
  });
