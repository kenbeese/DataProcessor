
function enable_link() {
  enable_projectlist_link();
  enable_project_link();
  enable_run_link();
  $("a.dp-nav") // do not off event
    .on("click", function(){
      $(this).parent("li").nextAll().remove();
      $(this).parent("li").remove();
    });
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
