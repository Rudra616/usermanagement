
function required(){
    var isValid = true;

    var errors = document.querySelectorAll("[class='error']");
    var name = document.getElementById('name').value
    var password = document.getElementById('password').value
    var all = [name, password]
    all.forEach((element,key) => {
    if(element === ''){
      errors[key].innerText ="This field is required";
      isValid = false;

    }
    });

    
    return isValid
}