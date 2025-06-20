  var stateDistrictMap = {
        "Gujarat": ["Ahmedabad", "Surat", "Rajkot"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur"]
      };

      var stateDropdown = document.getElementById("state");
      var districtDropdown = document.getElementById("district");

      stateDropdown.onchange = function() {
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
    
  
function required() {
    var FirstName = document.getElementById("FirstName").value
    var LastName = document.getElementById("LastName").value
    var username = document.getElementById("username").value
    var password = document.getElementById("password").value
    var email = document.getElementById("email").value
    var number = document.getElementById("number").value

    var address = document.getElementById("address").value
    var state = document.getElementById("state").value
    var district = document.getElementById("district").value

    var all = [FirstName, LastName, username, password, email, address, state, district];
    for (var i = 0; i < all.length; i++) {
    if (all[i] == '' ) {
      alert("Please fill all data.");
      return false;
        }
    }

    number = number.replace(/[^0-9]/g, '');
    if (number.length < 10 || number.length > 10) {
        alert("Wrong number. It must be exactly 10 digits.");
        document.getElementById("number").focus();
        return false;
    }    

    return true;
}

function characters(input){
    const A  = /[^a-zA-Z]/g;
    input.value = input.value.replace(A,'');
}


