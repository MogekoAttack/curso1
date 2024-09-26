function NewMessage() {
    let center = document.querySelectorAll(`#messages-center>*`)
    center.forEach( element => {
        element.style.display = `none`
    })
    document.querySelector(`#message-element`).style.display = `flex`
}

async function ProcessSend() {
    const receiver = document.getElementById('input-receiver').value
    const messageBody = document.getElementById('input-body').value

    console.log('Receiver:', receiver)
    console.log('Message:', messageBody)

    let body = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            receiver: receiver,
            messageBody: messageBody,
        })
    }

    let response = await fetch('/messages/', body).then(response => {
        return response.json()
    }).then(result => {
        return result
    });

    console.log(`1.- `);
    console.log(response);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function ViewMessage(id) {
    id = parseInt(id)

    let body = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }

    let response = await fetch(`/get_messages/?id=${id}`, body).then(response => {
        return response.json()
    }).then(result => {
        return result
    })

    if (response.status !== `success`) {
        return
    }

    let container = document.querySelector('#messages-center')

    let message = document.createElement('div')
    let message_sender = document.createElement('h3')
    let message_body = document.createElement('p')

    

}