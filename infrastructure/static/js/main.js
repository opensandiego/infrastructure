$(document).ready(function() {
  $( "form" ).on( "submit", function( event ) {
    event.preventDefault();
    form_data = $(this).serialize();
    $.ajax({
      url: '/projects_list',
      data: form_data,
    }).done(function(data) { 
      $('#project-list').html(data);
    });
  });
  $(document).on("click", ".remote #pagination a", function(event) {
    event.preventDefault();
    $('form #page').val($(this).data('page'));
    $('form').submit();
  });
  $('#projects_filter').on('click', '#submit', function(event) {
    $('form #page').val('1');
  });
  
});
