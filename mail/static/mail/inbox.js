document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#compose-form').addEventListener('submit', Enviar);
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function Enviar(evt) {
  evt.preventDefault();

  // Obtén los valores del formulario
  let destinatario = document.querySelector('#compose-recipients').value;
  let asunto = document.querySelector('#compose-subject').value;
  let mensaje = document.querySelector('#compose-body').value;

  // Haz una solicitud POST a '/emails'
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: destinatario,
        subject: asunto,
        body: mensaje,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
}