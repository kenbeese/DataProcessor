
function get_run(path) {
  $("section").hide(ANIMATION_SPEED);
  _sync_pipe_api_call({
    "name": "run_html",
    "args": [path,],
  }, function(html){
    $("section.dp-run")
      .empty()
      .append(html);
    enable_link();
    $(".dp-run").show(ANIMATION_SPEED);
  });
}

function enable_run_link() {
  $("a.dp-run")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      var name = $(this).text();
      get_run(path);
      if(! $(this).hasClass("dp-nav")){
        add_nav_link(path, name, "dp-run");
      }
    });
}
