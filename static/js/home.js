
$('#colorpicker').bcPicker();
$('#edit_colorpicker').bcPicker();

$('.bcPicker-palette').on('click', '.bcPicker-color', function(){
  var color = $(this).css('background-color');
  $(this).parent().parent().next().children().text($.fn.bcPicker.toHex(color));
  $(this).parent().parent().next().next().children().text(color);
  $('#color').val($.fn.bcPicker.toHex(color));
  $('#edit_color').val($.fn.bcPicker.toHex(color));
})


function fillModal(id, date, title, color, description, order) {
  $('#wsId').val(id);
  $('#edit_title').val(title);
  $('#edit_description').val(description);
  $('#edit_color').val(color);
  $('#edit_colorpicker').children('.bcPicker-picker').css('background-color', color);
  $('#edit_hex').children('span').text(color);
  $('#edit_order').val(order);
  $('#deleteWorkspace').attr('data-wsid', id);
}

$('#editWorkspaceButton').click(() => {
  $('#editWorkspaceForm').validate({
    rules: {
      wsId: {
        required: true
      },
      edit_title: {
        required: true
      },
      edit_description: {
        required: true
      },
      edit_color: {
        required: true
      },
      edit_order: {
        required: true
      }
    },
    submitHandler: ((form) => {
      $('#editWorkspaceButton').text("");
      $('#editWorkspaceButton').append(`<div class="spinner-border text-danger"></div>`);
      submitdata = {
        'wsId': form.wsId.value,
        'title': form.edit_title.value, 
        'description': form.edit_description.value, 
        'color': form.edit_color.value,
        'order': form.edit_order.value,
      }
      console.log(submitdata);
      $.ajax({
        type: 'post', 
        url: $SCRIPT_ROOT + '/editWorkspace', 
        data: JSON.stringify(submitdata), // stringyfy before passing
        dataType: 'json', // payload is json
        contentType: 'application/json',
        success: function (data) {
            if(data.result > 0){
              window.location.reload();
            }
          }
      });
    })
  })
});

$('#deleteWorkspace').click(() => {
  var wsId = $('#deleteWorkspace').attr('data-wsid');
  $('#deleteWorkspace').html(`<span class="spinner-border spinner-border-sm"></span>`);
  console.log(wsId)
  $.post($SCRIPT_ROOT + '/deleteWorkspace', {
    'wsId': wsId
  }).then((data) => {
    if(data == "Ok"){
      window.location.reload();
    } else {
      console.log("Error")
    }
  });
})