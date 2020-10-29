function clearMessage() {
  $('#my-toast').remove();
}

function showMessage(title = '', body = '', complement = '', autohide = false) {
  let message = ` <div id="my-toast" data-autohide="${autohide}" data-delay="4000" class="toast my-toast" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header bg-warning">
    <strong class="mr-auto text-dark"> ${title} </strong>
    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    </div>
    <div class="toast-body bg-warning">
      <p class="text-dark"> ${body} </p>
      ${complement}
    </div>
  </div>`
  clearMessage();
  $('body').append(message);
  $('#my-toast').toast('show');
}

$('#my-toast').on('hidden.bs.toast', function () {
  $('#my-toast').remove(); //remove da tela, para que não atrapalhe
}) 

function showErrorMessage(error) {
  console.warn(error);
  let title = 'Não foi possível completar a solicitação.';
  let body = 'Um erro desconhecido impediu que sua solicitação fosse completada. Tente novamente.';
  showMessage(title, body, undefined, true);
}