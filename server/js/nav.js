
function add_nav_link(path, name, classname) {
    var li$ = $("<li>").appendTo("ol#LocationBar");
    $("<a>")
      .addClass(classname)
      .addClass("dp-nav")
      .attr("dp-path", path)
      .append(name)
      .appendTo(li$);
}

function enable_nav_link() {
  $("a.dp-nav")
    .on("click", function(){
      $(this).parent("li").nextAll().remove();
    });
}

function enable_link() {
  $("a").off("click");
  enable_projectlist_link();
  enable_project_link();
  enable_run_link();
  enable_nav_link();
  enable_editable_comment();
}

function _sync_api_call(data, callback){
  $.blockUI(BLOCK_SETTING);
  $.ajax({
    url: API_URL,
    type: "POST",
    data: data,
    success: function(res, st){
      if("exit_code" in res && res["exit_code"] != 0){
        alert("Server Error: " + res["message"]);
      }
      callback(res);
    },
    error: function(xhr, st, error){
      alert("Server connection failed");
    },
    complete: function(xhr, st){
      $.unblockUI();
    },
  });
}
