
var api_url = "/cgi-bin/api.cgi"

function get_project_list() {
  $.post(api_url, {
      "type": "pipe", 
      "name": "projects_html",
      "args": "[]", 
    }, function (res) {
      paths = res["paths"];
      html = res["html"];
      $("section.dp-projectlist").append(html);
    }
  );
}

function show_project_list(){
  $(".dp-project").hide();
  $(".dp-run").hide();
  $(".dp-projectlist").show();
}

$(function(){
  get_project_list();
  show_project_list();
});
