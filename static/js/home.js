$( document ).ready(function() {
    console.log('sa');
    $.getJSON($SCRIPT_ROOT + '/users', {}, function(data) {
      console.log(data)
    });
    console.log('as');
    return false;
});

