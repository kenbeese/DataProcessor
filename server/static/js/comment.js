
function send_comment(comment, path){
  /** send comment to server */
    $.ajax({
        url: PIPE_API_URL,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "name": "add_comment",
            "args": [comment, path],
        }),
        success: function(res){
            // alert("comment update");
        },
        error: function(xhr, st, error){
            alert("Server connection failed");
        },
    });
}

function enable_editable_comment() {
  f_click = function(){
    var comment = $(this).text();
    var path = $(this).attr("dp-path");
    $(this).empty().off("click");
    $("<textarea>")
      .val(comment)
      .attr("dp-path", path)
      .addClass("form-control")
      .appendTo(this)
      .focus();
  };
  f_blur = function(){
    var comment = $(this).val();
    var path = $(this).attr("dp-path");
    send_comment(comment, path);
    $(this).parent()
      .empty()
      .text(comment)
      .on("click", f_click);
  };
  $(".dp-comment")
    .off("click")
    .on("click", f_click)
    .off("blur", "textarea")
    .on("blur", "textarea", f_blur);
}
