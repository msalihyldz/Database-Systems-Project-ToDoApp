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

$(function() {
  /* Rounded Dots Dark */
  $("#content-1").mCustomScrollbar({
    theme: "rounded-dots-dark"
  });

  /* Rounded Dark */
  $("#content-2").mCustomScrollbar({
    theme: "rounded-dark"
  });

  /* Inset Dark */
  $("#content-3").mCustomScrollbar({
    theme: "inset-3-dark"
  });

  /* 3d Dark */
  $("#content-4").mCustomScrollbar({
    theme: "3d-dark"
  });

  /* Dark Thin */
  $("#content-5").mCustomScrollbar({
    theme: "dark-thin"
  });
});
