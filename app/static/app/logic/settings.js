$('#change-settings-modal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget);
    const key = button.data('key');
    const value = button.data('value');

    const modal = $(this)
    modal.find('.modal-title').text('Change your ' + key);
    modal.find('.modal-body input').attr("placeholder", value);
    modal.find('.code').val(key);
    modal.find('.modal-body input').val("");
    modal.find('.modal-change-button').text('Change ' + key);
})
