
function get_project_list() {
  _sync_api_call({
    "type": "pipe",
    "name": "projectlist_html",
    "args": "[]",
  }, function(res){
    paths = res["paths"];
    html = res["html"];
    $("section.dp-projectlist")
      .empty()
      .append(html);
    enable_project_link();
    enable_editable_comment();
  })
}

function show_project_list(){
  $("section.dp-project").hide(animation_speed);
  $("section.dp-run").hide(animation_speed);
  $(".dp-projectlist").show(animation_speed);
  $("a.dp-project").show(animation_speed);
}

$(function(){
  get_project_list();
  show_project_list();
  $("a.dp-projectlist")
    .off("click")
    .on("click", function(){
      get_project_list();
      show_project_list();
    });
});
