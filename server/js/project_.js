
function get_project(path) {
  $("section.dp-project").empty();
  _sync_api_call({
    "type": "pipe",
    "name": "project_html",
    "args": JSON.stringify([path,]),
  }, function(res){
    var name = res["name"];
    var table_html = res["html"];
    $("section.dp-project").append(table_html);
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .attr("dp-path", path)
      .append(name)
      .appendTo(li$);
    enable_project_link();
    enable_editable_comment();
  });
}

function show_project(){
  $("section.dp-projectlist").hide(ANIMATION_SPEED);
  $("section.dp-run").hide(ANIMATION_SPEED);
  $("a.dp-projectlist").show(ANIMATION_SPEED);
  $("a.dp-run").show(ANIMATION_SPEED);
  $(".dp-project").show(ANIMATION_SPEED);
}

function enable_project_link(){
  $("a.dp-project")
    .off("click")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      get_project(path);
      show_project();
    });
  _enable_nav();
}
