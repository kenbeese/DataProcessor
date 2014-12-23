
function get_project(path) {
  $("section.dp-project").empty();
  $.post(api_url, {
      "type": "pipe", 
      "name": "project_html",
      "args": JSON.stringify([path,]), 
    }, function (res) {
      var name = res["name"];
      var table_html = res["html"];
      $("section.dp-project")
        .empty()
        .append(table_html);
      var li$ = $("<li>").appendTo("ol#LocationBar");
      $("<a>")
        .attr("dp-path", path)
        .append(name)
        .appendTo(li$);
      enable_project_link();
      enable_editable_comment();
      $.unblockUI();
      show_project();
    }
  );
}

function show_project(){
  $("section.dp-projectlist").hide(animation_speed);
  $("section.dp-run").hide(animation_speed);
  $("a.dp-projectlist").show(animation_speed);
  $("a.dp-run").show(animation_speed);
  $(".dp-project").show(animation_speed);
}

function enable_project_link(){
  $("a.dp-project")
    .off("click")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      $.blockUI();
      get_project(path);
    });
  _enable_nav();
}
