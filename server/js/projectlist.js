
function get_project_list() {
  $("section.dp-projectlist").empty();
  _sync_api_call({
    "type": "pipe",
    "name": "projectlist_html",
    "args": "[]",
  }, function(res){
    paths = res["paths"];
    html = res["html"];
    $("section.dp-projectlist").append(html);
    enable_project_link();
    enable_editable_comment();
    var table = $("table.dp-projectlist").DataTable(DATATABLES_SETTING);
  })
}

function show_project_list(){
  $("section.dp-project").hide(ANIMATION_SPEED);
  $("section.dp-run").hide(ANIMATION_SPEED);
  $(".dp-projectlist").show(ANIMATION_SPEED);
  $("a.dp-project").show(ANIMATION_SPEED);
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
