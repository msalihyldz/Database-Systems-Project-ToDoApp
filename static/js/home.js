$( document ).ready(function() {
    $(function() {
        $('a#calculate').bind('click', function() {
          $.getJSON($SCRIPT_ROOT + '/users', {}, function(data) {
            console.log(data)
          });
          return false;
        });
      });
})