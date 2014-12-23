
function _enable_nav() {
  /** enable dp-nav which clears display history in location bar
   *
   * This must be called from enable_*_link
   */
  $("a.dp-nav") // do not off event
    .on("click", function(){
      $(this).parent("li").next().remove();
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
