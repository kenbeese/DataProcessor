
function send_comment(comment, path){
  /** send comment to server */
  $.post("/cgi-bin/api.cgi", {
      "type": "pipe",
      "name": "add_comment",
      "args": JSON.stringify([comment, path])
    }, function(res){
      // alert("comment update");
    }
  );
}

function enable_editable_comment() {
  f_click = function(){
    var comment = $(this).text();
    var path = $(this).attr("dp-path");
    $(this).empty().off("click");
    $("<textarea>")
      .addClass("dp-comment")
      .val(comment)
      .attr("dp-path", path)
      .appendTo(this)
      .focus();
  };
  f_blur = function(){
    var comment = $(this).val();
    var path = $(this).attr("dp-path");
    send_comment(comment, path);
    $(this).parent()
      .empty()
      .append(comment)
      .on("click", f_click);
  };
  $("td.dp-comment")
    .off("click")
    .on("click", f_click)
    .off("blur", "textarea.dp-comment")
    .on("blur", "textarea.dp-comment", f_blur);
}
