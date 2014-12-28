
function get_project(path) {
  $("section").hide(ANIMATION_SPEED);
  _sync_api_call({
    "type": "pipe",
    "name": "project_html",
    "args": JSON.stringify([path,]),
  }, function(res){
    var name = res["name"];
    var table_html = res["html"];
    $("section.dp-project")
      .empty()
      .append(table_html);
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .addClass("dp-project")
      .addClass("dp-nav")
      .attr("dp-path", path)
      .append(name)
      .appendTo(li$);
    enable_link();
    $("table.dp-project").DataTable(DATATABLES_SETTING);
    $(".dp-project").show(ANIMATION_SPEED);
  });
}

function enable_project_link(){
  $("a.dp-project")
    .off("click")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      get_project(path);
    });
}
