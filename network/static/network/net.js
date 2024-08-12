document.addEventListener("DOMContentLoaded", async (evt) => {
    let elements = document.querySelectorAll(`.btn-link-global`);
    for (const element of elements) {
        let verificar_like = await Verificar(element.id.toString().split(`boton-like-post`)[1]);
        verificar_like[`like`] === 1 ? element.innerText = `Unlike` : false;
    }
});

function Editar(id){
    let original = document.getElementById(id);
    let nuevo = document.createElement(`textarea`);
    
    document.getElementById(`boton-editar-${id}`).innerText = `Guardar`;
    document.getElementById(`boton-editar-${id}`).setAttribute(`onclick`, `Guardar('${id}')`);

    nuevo.id = `textarea-edit-${id.split(`-`)[0].split(`post`)[1]}`;
    nuevo.style.width = `100%`;
    nuevo.textContent = original.textContent;

    original.parentNode.replaceChild(nuevo, original);
}

async function Guardar(id) {
    let textarea = document.getElementById(`textarea-edit-${id.split(`-`)[0].split(`post`)[1]}`);
    let texto = textarea.value;
    console.log('texto: ', texto);

    let a = await fetch(`http://localhost:8000/edit/${id.split(`-`)[0].split(`post`)[1]}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'texto': texto
        })
    }).then(response => response.json()).then(data => {
        return data;
    }).catch((error) => {
        console.error('Error:', error);
    });

    if (a['success'] !== true){
        return false
    }

    let nuevo = document.createElement(`p`);
    nuevo.id = `post${id.split(`-`)[0].split(`post`)[1]}-${id.split(`-`)[1]}`;
    nuevo.textContent = texto;

    textarea.parentNode.replaceChild(nuevo, textarea);

    document.getElementById(`boton-editar-${id}`).innerText = `Editar`;
    document.getElementById(`boton-editar-${id}`).setAttribute(`onclick`, `Editar('${id}')`);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function Like(id){
    await fetch(`/like/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    }).then(response =>{
        return response.json();
    }).then(data => {
        console.log('data: ', data);
        return data;
    });
    let datos = await Verificar(id);
    if (datos[`like`] === 1) {
        document.getElementById(`boton-like-post${id}`).innerText = `Unlike`;
    } else {
        document.getElementById(`boton-like-post${id}`).innerText = `Like`;
    }
    document.getElementById(`likes-post${id}`).innerText = `Likes: ${datos['num_likes'].toString()}`;
}



async function Verificar(id){
    let datos = await fetch(`/verificar/${id}/`).then(response =>{
        return response.json();
    }).then(data => {
        return data;
    });
    console.log('datos: ', datos);
    return datos;
}