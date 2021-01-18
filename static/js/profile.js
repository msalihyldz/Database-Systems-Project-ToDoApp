
$('#updateUserButton').click(() => {
    $('#updateUserForm').validate({
        rules: {
          uId: {
            required: true
          },
          edit_name: {
            required: true
          },
          edit_surname: {
            required: true
          }
        },
        submitHandler: ((form) => {
          $('#updateUserButton').text("");
          $('#updateUserButton').append(`<div class="spinner-border text-danger"></div>`);
          submitdata = {
            'uId': form.uId.value,
            'name': form.edit_name.value, 
            'surname': form.edit_surname.value,
          }
          console.log(submitdata);
          $.ajax({
            type: 'post', 
            url: $SCRIPT_ROOT + '/editUser', 
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
})

$('#deleteMyAccount').click(() => {
    $('#delete').text("");
    $('#delete').append(`<div class="spinner-border text-danger"></div>`);
    $('#deleteAccount').modal("hide");
    console.log('sa');
    $.post("/deleteUser").then((data) => {
        if(data.result == "Ok"){
            console.log('sa');
            window.location = "/login";
        }
    });
})