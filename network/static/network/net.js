document.addEventListener("DOMContentLoaded", evt =>{
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
            // ¿Este cookie empieza con el nombre que estamos buscando?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
