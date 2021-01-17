
$( document ).ready(function() {
  var maxHeight = 0;
  $('.ws-list').each(function() {
    if($(this).height() > maxHeight){
      console.log($(this).height());
      maxHeight = $(this).height();
    }
  });
  $('.ws-list').height(maxHeight);
});
$(function() {
    $('a#testButton').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/getTheNumber',
          function(data) {
        //do nothing
      });
      return false;
    });
})



$(function () {
  // INITIALIZE DATEPICKER PLUGIN
  $('#endDate').datepicker({
      clearBtn: true,
      dateFormat: 'dd/mm/yy',
      minDate:  0,
      onSelect: function(date){
          var date1 = $('#endDate').datepicker('getDate');
          console.log(date1);
      }
  });

});

$('#endDate').click(() => {
  $('#ui-datepicker-div').css('z-index',1100);
})

$(function () {
  // INITIALIZE DATEPICKER PLUGIN
  $('#edit_endDate').datepicker({
      clearBtn: true,
      dateFormat: 'dd/mm/yy',
      onSelect: function(date){
          var date1 = $('#edit_endDate').datepicker('getDate');
          console.log(date1);
      }
  });

});

$('#edit_endDate').click(() => {
  $('#ui-datepicker-div').css('z-index',1100);
})

$('#addTaskButton').click(() => {
  $('#addTaskForm').validate({
    rules: {
      content: {
        required: true
      },
      listId: {
        required: true
      },
      assignedId: {
        required: true
      },
      endDate: {
        required: true
      },
      importance: {
        required: true
      },
      listorder: {
        required: true
      }
    },
    messages: {
      content: {
        required: "Content cannot be empty!"
      },
      listId: {
        required: "List cannot be empty!"
      },
      assignedId: {
        required: "Assigned cannot be empty!"
      },
      endDate: {
        required: "Deadline cannot be empty!"
      },
      importance: {
        required: "Importance cannot be empty!"
      },
      listorder: {
        required: "Order cannot be empty!"
      }
    },
    submitHandler: ((form) => {
      console.log(form.content.value);
      $('#addTaskButton').text("");
      $('#addTaskButton').append(`<div class="spinner-border text-danger"></div>`);
      $.post($SCRIPT_ROOT + '/addTask', {
        'content': form.content.value, 
        'listId': form.listId.value, 
        'assignedId':form.assignedId.value,
        'endDate': form.endDate.value,
        'importance': form.importance.value,
        'listorder': form.listorder.value
      }).then((data) => {
        if(data){
          window.location.reload();
        }
      });
    })
  })
});

function fillModal(id, content, listid, assignedid, date, isDone, importance, listorder) {
  $('#taskId').val(id);
  $('#edit_content').val(content);
  $('#edit_listId').val(listid);
  $('#edit_assignedId').val(assignedid);
  date = date.split(" ")[0];
  date = date.split("-");
  date = new Date(date[0],date[1]-1, date[2]);
  $('#edit_endDate').datepicker('setDate', date);
  if(isDone == 'True'){
    $('#edit_isDone').prop('checked', true)
  }
  $('#edit_importance').val(importance);
  $('#edit_listorder').val(listorder);
  $('#deleteTask').attr('data-taskid', id);
}

$('#editTaskButton').click(() => {
  $('#editTaskForm').validate({
    rules: {
      taskId: {
        required: true
      },
      edit_content: {
        required: true
      },
      edit_listId: {
        required: true
      },
      edit_assignedId: {
        required: true
      },
      edit_endDate: {
        required: true
      },
      edit_importance: {
        required: true
      },
      edit_listorder: {
        required: true
      }
    },
    submitHandler: ((form) => {
      $('#editTaskButton').text("");
      $('#editTaskButton').append(`<div class="spinner-border text-danger"></div>`);
      submitdata = {
        'taskId': form.taskId.value,
        'content': form.edit_content.value, 
        'listId': form.edit_listId.value, 
        'assignedId': form.edit_assignedId.value,
        'endDate': form.edit_endDate.value,
        'isDone': form.edit_isDone.value == "on" ? true : false,
        'importance': form.edit_importance.value,
        'listorder': form.edit_listorder.value
      }
      $.ajax({
        type: 'post', 
        url: $SCRIPT_ROOT + '/editTask', 
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

$('#addListButton').click(() => {
  $('#addListForm').validate({
    rules: {
      title: {
        required: true
      }
    },
    messages: {
      title: {
        required: "Title cannot be empty!"
      }
    },
    submitHandler: ((form) => {
      console.log(form.listTitle.value)
      $('#addListButton').text("");
      $('#addListButton').append(`<div class="spinner-border text-danger"></div>`);
      $.post($SCRIPT_ROOT + '/addList', {
        'title': form.listTitle.value,
        'wid': form.wid.value
      }).then((data) => {
        if(data == "Ok"){
          window.location.reload();
        }
      });
    })
  })
});

$('#btnAddUser').click(() => {
  userMail = $('#addUser').val();
  wid = $('#wsId').val();
  $('#btnAddUser').text("");
  $('#btnAddUser').append(`<div class="spinner-border text-danger"></div>`);
  $.post($SCRIPT_ROOT + '/addFriend', {
    'email': userMail,
    'wid': wid
  }).then((data) => {
    if(data == "Not Found"){
      $('#addUser').val('');
      $('#addUser').attr("placeholder", "User could not find!");
      $('#addUser').css("border-color", "red");
    } else if(data == "Ok"){
      window.location.reload();
    }
    $('#btnAddUser').empty();
    $('#btnAddUser').text("Add");
    /*if(data == "Ok"){
      window.location.reload();
    }*/
  });
})

$('.listcomments').hide();

function open_close(id){
  var clist = $('.listcomments[data-taskid = ' + id + ']');
  if(clist.is(":visible")){
    clist.prev().children("u").children("i").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    clist.hide();
  } else {
    clist.prev().children("u").children("i").removeClass("fa-chevron-down").addClass("fa-chevron-up");
    clist.show();
  }
}

function addComment(taskId){
  var input = $('input[data-taskid = ' + taskId + ']');
  var content = input.val();
  input.next().html(`<span class="spinner-border spinner-border-sm"></span>`);
  $.post($SCRIPT_ROOT + '/addComment', {
    'content': content,
    'taskId': taskId
  }).then((data) => {
    if(data == "Ok"){
      window.location.reload();
    } else {
      console.log("Error")
    }
  });
}

$('#deleteTask').click(() => {
  var taskId = $('#deleteTask').attr('data-taskid');
  $('#deleteTask').html(`<span class="spinner-border spinner-border-sm"></span>`);
  $.post($SCRIPT_ROOT + '/deleteTask', {
    'taskId': taskId
  }).then((data) => {
    if(data == "Ok"){
      window.location.reload();
    } else {
      console.log("Error")
    }
  });
})