function Botones(){
    // LOGIN
    // document.querySelector(`#login-button`).addEventListener(`click`, ()=> Login())
}

async function Login(){
    let username = document.querySelector(`#login-username`).value
    // let password = document.querySelector(`#login-password`).value

    let user_exist = await fetch(`/login/${username}`).then(response => {
        return response.json()
    }).then(response => {
        return response
    }).catch(error => {
        console.error(`UPS! (-1)`)
        console.log(error)
    })

    if (user_exist[`response`]){
        alert(`This username exist!`)
        window.open(`/login/true`, `_self`)
    } else {
        alert(`This username not exist!`)
    }
}