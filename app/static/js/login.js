
function required(){
    var name = document.getElementById('name').value
    var password = document.getElementById('password').value
    if(name == '' || password== ''){
        alert('right user name or password')
        return false
    }
    return true
}