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




