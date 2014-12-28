
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
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .addClass("dp-projectlist")
      .addClass("dp-nav")
      .append("Project List")
      .appendTo(li$);
    enable_link();
    $("table.dp-projectlist").DataTable(DATATABLES_SETTING);
    $(".dp-projectlist").show(ANIMATION_SPEED);
  })
}

function enable_projectlist_link() {
  $("a.dp-projectlist")
    .off("click")
    .on("click", function(){
      get_projectlist();
    });
}

$(function(){
  get_projectlist();
});
