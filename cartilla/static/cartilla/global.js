document.addEventListener(`DOMContentLoaded`, function (){
    Botones()
})

function Botones(){
    // LAYOUT
    document.querySelector(`#layout-index-btn`).addEventListener(`click`, ()=> window.open(`/`, `_self`))
    if (document.querySelector(`#layout-login-btn`)) {
        document.querySelector(`#layout-login-btn`).addEventListener(`click`, ()=> window.open(`/login/`, `_self`))
    }
}