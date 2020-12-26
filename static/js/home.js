
$(function() {
    $.getJSON($SCRIPT_ROOT + '/users', {}, function(data) {
      console.log(data)
    });
    return false;
});