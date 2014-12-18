
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
    $(this).empty().off("click")
    $("<input>")
      .addClass("dp-comment")
      .attr("value", comment)
      .attr("dp-path", path)
      .appendTo(this)
      .focus();
  }
  f_blur = function(){
    var comment = $(this).val();
    var path = $(this).attr("dp-path");
    send_comment(comment, path);
    $(this).parent()
      .empty()
      .append(comment)
      .on("click", f_click);
  }
  $("td.dp-comment")
    .off("click")
    .on("click", f_click)
    .off("blur", "input.dp-comment")
    .on("blur", "input.dp-comment", f_blur);
}
