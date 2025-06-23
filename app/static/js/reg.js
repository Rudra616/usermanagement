var stateDistrictMap = {
  Gujarat: ["Ahmedabad", "Surat", "Rajkot"],
  Maharashtra: ["Mumbai", "Pune", "Nagpur"],
  Rajasthan: ["Jaipur", "Udaipur", "Jodhpur"],
};

var stateDropdown = document.getElementById("state");
var districtDropdown = document.getElementById("district");

stateDropdown.onchange = function () {
  var selectedState = stateDropdown.value;

  var districts = stateDistrictMap[selectedState];

  districtDropdown.innerHTML = "";

  var defaultOption = document.createElement("option");
  defaultOption.text = "-- Select District --";
  defaultOption.value = "";
  districtDropdown.add(defaultOption);

  if (districts) {
    for (var i = 0; i < districts.length; i++) {
      var option = document.createElement("option");
      option.text = districts[i];
      option.value = districts[i];
      districtDropdown.add(option);
    }
  }
};

function isFormValid() {
  var errors = document.querySelectorAll("[class='error']");
  var FirstName = document.getElementById("FirstName").value;
  var LastName = document.getElementById("LastName").value;
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var number = document.getElementById("number").value;
  var email = document.getElementById("email").value;
  var address = document.getElementById("address").value;
  var state = document.getElementById("state").value;
  var district = document.getElementById("district").value;

  var all = [
    FirstName,
    LastName,
    username,
    password,
    number,
    email,
    address,
    state,
    district,
  ];
  var isValid = true;

  //clear all error messages 
  errors.forEach((element,key )=> {
    errors[key].innerText ='';
  }); 
 
  // check for not empty
  all.forEach((element,key) => {
    if(element === ''){
      errors[key].innerText ="This field is required";
      isValid = false;
    }
  });
 
  var cleanedNumber = number.replace(/[^0-9]/g, "");
  if (cleanedNumber.length !== 10) {
    errors[4].innerText = "Number must be exactly 10 digits";
    document.getElementById("number").focus();  
    isValid = false;
  }
  
  return isValid;
}

function onlyAcceptAlphabets(input) { 
  input.value = input.value.replace(/[^a-zA-Z]/g, "");
}
