$(document).ready(function(){
  $("#prospect-table-search").on("keyup", function() {
    let value = $(this).val().toLowerCase();
    $("#prospect-table-body tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});