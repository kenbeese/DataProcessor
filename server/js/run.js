
function get_run(path) {
  $("section.dp-run").empty();
  _sync_api_call({
    "type": "pipe",
    "name": "run_html",
    "args": JSON.stringify([path,]),
  }, function(res){
    var name = res["name"];
    var html = res["html"];
    $("section.dp-run").append(html);
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .addClass("dp-run")
      .addClass("dp-nav")
      .attr("dp-path", path)
      .append(name)
      .appendTo(li$);
    enable_link();
  });
}

function show_run() {
  $("section.dp-projectlist").hide(ANIMATION_SPEED);
  $("section.dp-project").hide(ANIMATION_SPEED);
  $(".dp-run").show(ANIMATION_SPEED);
}

function enable_run_link() {
  $("a.dp-run")
    .off("click")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      get_run(path);
      show_run();
    });
}
