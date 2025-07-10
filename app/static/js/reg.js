
  function showLoader() {
    document.getElementById("loader").style.display = "block";
}

function hideLoader() {
    document.getElementById("loader").style.display = "none";
}
  

function onlyAcceptAlphabets(input) {
  input.value = input.value.replace(/[^a-zA-Z]/g, "");
}

function isFormValid() {
  var errors = document.querySelectorAll("small.error");
  var fields = [
    document.getElementById("FirstName").value,
    document.getElementById("LastName").value,
    document.getElementById("username").value,
    document.getElementById("password").value,
    document.getElementById("number").value,
    document.getElementById("email").value,
    document.getElementById("address").value,
    document.getElementById("state").value,
    document.getElementById("district").value,
  ];

  var isValid = true;

  errors.forEach((e, i) => e.innerText = "");

  fields.forEach((field, i) => {
    if (!field.trim()) {
      errors[i].innerText = "This field is required";
      isValid = false;
    }
  });

  const number = document.getElementById("number").value;
  if (number.length !== 10) {
    errors[4].innerText = "Number must be exactly 10 digits";
    isValid = false;
  }

  return isValid;
}

// 🔄 Fetch districts dynamically when state changes
document.getElementById("state").addEventListener("change", function () {
  const stateId = this.value;
  const districtDropdown = document.getElementById("district");

  districtDropdown.innerHTML = '<option value="">Loading...</option>';

  fetch(`/get-districts/?state_id=${stateId}`)
    .then(response => response.json())
    .then(data => {
      districtDropdown.innerHTML = '<option value="">-- Select District --</option>';
      data.forEach(d => {
        const option = document.createElement("option");
        option.value = d.id;
        option.text = d.name;
        districtDropdown.appendChild(option);
      });
    })
    .catch(error => {
      console.error('Error fetching districts:', error);
      districtDropdown.innerHTML = '<option value="">-- Select state--</option>';
    });
});

// ✅ AJAX form submit with validation
document.getElementById("registerForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const form = this;

  if (!isFormValid()) return;
  showLoader()
  const formData = new FormData(form);
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  fetch(form.action || window.location.href, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest"
    },
    body: formData
  })
   
  .then(response => response.json())
  .then(data => {
    document.querySelectorAll(".alert").forEach(el => el.remove());

    const alertBox = document.createElement("div");
    alertBox.classList.add("alert", data.success ? "alert-success" : "alert-danger");
    alertBox.innerText = data.message || data.error;

    form.insertAdjacentElement("beforebegin", alertBox);

    if (data.success) {
      form.reset();
      document.getElementById("district").innerHTML = '<option value="">-- Select District --</option>';
    }
      hideLoader(); 
  })
  .catch(error => {
    console.error("Error submitting form:", error);
    alert("An error occurred. Please try again.");
  });
});
