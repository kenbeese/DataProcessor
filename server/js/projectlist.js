
var api_url = "/cgi-bin/api.cgi"

function get_project_list() {
  $.post(api_url, {
      "type": "pipe", 
      "name": "projectlist_html",
      "args": "[]", 
    }, function (res) {
      paths = res["paths"];
      html = res["html"];
      $("section.dp-projectlist")
        .empty()
        .append(html);
      enable_project_link();
      enable_editable_comment();
      $.unblockUI();
    }
  );
}

function show_project_list(){
  $("section.dp-project").hide();
  $("section.dp-run").hide();
  $(".dp-projectlist").show();
  $("a.dp-project").show();
}

$(function(){
  get_project_list();
  show_project_list();
  $("a.dp-projectlist")
    .off("click")
    .on("click", function(){
      $.blockUI();
      get_project_list();
      show_project_list();
    });
});
