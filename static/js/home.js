
$('#colorpicker').bcPicker();

$('.bcPicker-palette').on('click', '.bcPicker-color', function(){
  var color = $(this).css('background-color');
  $(this).parent().parent().next().children().text($.fn.bcPicker.toHex(color));
  $(this).parent().parent().next().next().children().text(color);
  $('#color').val($.fn.bcPicker.toHex(color));
})