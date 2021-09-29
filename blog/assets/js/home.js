
function login(){
    var username=document.getElementById('exampleInputEmail1').value 
    var password=document.getElementById('exampleInputPassword1').value
    var csrf=document.getElementById('csrf').value 


    if(username == '' || password == ''){
        alert('Must Enter Both Fields')
    }

    data={
        'username': username,
        'password': password
    }

    fetch('/api/login/',{
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify(data)
    }).then(result => result.json())
    .then(response => {

        console.log(response)

        /*if(response['status'] == 200){
            window.location.href= '/'
        }*/
    })
}
