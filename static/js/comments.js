$(function () {

  /* Functions */

  let loadForm = function () {
    let btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-form .modal-content").html("");
        $("#modal-form").modal("show");
      },
      success: function (data) {
        $("#modal-form .modal-content").html(data.html_form);
      }
    });
  };

  let saveForm = function () {
    let form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#comment-table div").html(data.html_comment_list);
          $("#modal-form").modal("hide");
        }
        else {
          $("#modal-form .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create comment
  $(".js-create-comment").click(loadForm);
  $("#modal-form").on("submit", ".js-comment-create-form", saveForm);

  $(".js-load-comments").click(loadForm);

  // Update book
  // $("#book-table").on("click", ".js-update-book", loadForm);
  // $("#modal-form").on("submit", ".js-book-update-form", saveForm);
  //
  // // Delete book
  // $("#book-table").on("click", ".js-delete-book", loadForm);
  // $("#modal-form").on("submit", ".js-book-delete-form", saveForm);

});