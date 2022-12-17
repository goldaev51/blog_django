$(function () {

    /* Functions */

    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-form-comment .modal-content").html("");
                $("#modal-form-comment").modal("show");
            },
            success: function (data) {
                $("#modal-form-comment .modal-content").html(data.html_form);
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
                    // $("#comment-table div").html(data.html_comment_list);
                    $("#modal-form-comment").modal("hide");
                } else {
                    $("#modal-form-comment .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    let loadFeedbackForm = function () {
        let a = $(this);
        $.ajax({
            url: a.attr("data-url"),
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

    let saveFeedbackForm = function () {
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#modal-form").modal("hide");
                } else {
                    $("#modal-form .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create comment
    $(".js-create-comment").click(loadForm);
    $("#modal-form-comment").on("submit", ".js-comment-create-form", saveForm);

    $("a.js-create-feedback").click(loadFeedbackForm);
    $("#modal-form").on("submit", ".js-feedback-create-form", saveFeedbackForm);

});