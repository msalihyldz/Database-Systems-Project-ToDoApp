$( document ).ready(function() {
    console.log( "ready!" );
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


  $(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });
