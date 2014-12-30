
function get_projectlist() {
  $("section").hide(ANIMATION_SPEED);
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
    enable_link();
    $("table.dp-projectlist").DataTable(DATATABLES_SETTING);
    $(".dp-projectlist").show(ANIMATION_SPEED);
  })
}

function enable_projectlist_link() {
  $("a.dp-projectlist")
    .on("click", function(){
      get_projectlist();
    });
}

$(function(){
  get_projectlist();
});
