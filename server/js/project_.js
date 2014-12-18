
var api_url = "/cgi-bin/api.cgi"

function get_project(path) {
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
  _enable_nav();
}
