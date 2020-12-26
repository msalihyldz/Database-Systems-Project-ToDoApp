$( document ).ready(function() {
    console.log('sa');
    $.getJSON($SCRIPT_ROOT + '/users', {}, function(data) {
      console.log(data)
    });
    return false;
});
