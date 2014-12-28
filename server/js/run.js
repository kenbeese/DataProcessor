
function get_run(path) {
  $("section").hide(ANIMATION_SPEED);
  _sync_api_call({
    "type": "pipe",
    "name": "run_html",
    "args": JSON.stringify([path,]),
  }, function(res){
    var name = res["name"];
    var html = res["html"];
    $("section.dp-run")
      .empty()
      .append(html);
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .addClass("dp-run")
      .addClass("dp-nav")
      .attr("dp-path", path)
      .append(name)
      .appendTo(li$);
    enable_link();
    $(".dp-run").show(ANIMATION_SPEED);
  });
}

function enable_run_link() {
  $("a.dp-run")
    .off("click")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      get_run(path);
    });
}
