
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
      .addClass("dp-project")
      .addClass("dp-nav")
      .attr("dp-path", path)
      .append(name)
      .appendTo(li$);
    enable_link();
    enable_editable_comment();
    $("table.dp-project").DataTable(DATATABLES_SETTING);
  });
}

function show_project(){
  $("section.dp-projectlist").hide(ANIMATION_SPEED);
  $("section.dp-run").hide(ANIMATION_SPEED);
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
}
