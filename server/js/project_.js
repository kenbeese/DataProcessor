
var api_url = "/cgi-bin/api.cgi"

function get_project(path) {
  $.post(api_url, {
      "type": "pipe", 
      "name": "project_table_html",
      "args": JSON.stringify([path,]), 
    }, function (table_html) {
      $("section.dp-project")
        .empty()
        .append(table_html);
      $("ol#LocationBar>li>a.dp-project")
        .empty()
        .attr("dp-path", path)
        .append(path); // TODO should be name
    }
  );
}

function show_project(){
  $("section.dp-projectlist").hide();
  $("section.dp-run").hide();
  $("a.dp-projectlist").show();
  $("a.dp-run").show();
  $(".dp-project").show();
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
