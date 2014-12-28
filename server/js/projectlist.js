
function get_projectlist() {
  $("section.dp-projectlist").empty();
  _sync_api_call({
    "type": "pipe",
    "name": "projectlist_html",
    "args": "[]",
  }, function(res){
    paths = res["paths"];
    html = res["html"];
    $("section.dp-projectlist").append(html);
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .addClass("dp-projectlist")
      .addClass("dp-nav")
      .append("Project List")
      .appendTo(li$);
    enable_link();
    $("table.dp-projectlist").DataTable(DATATABLES_SETTING);
  })
}

function show_projectlist(){
  $("section.dp-project").hide(ANIMATION_SPEED);
  $("section.dp-run").hide(ANIMATION_SPEED);
  $(".dp-projectlist").show(ANIMATION_SPEED);
}

function enable_projectlist_link() {
  $("a.dp-projectlist")
    .off("click")
    .on("click", function(){
      get_projectlist();
      show_projectlist();
    });
}

$(function(){
  get_projectlist();
  show_projectlist();
});
