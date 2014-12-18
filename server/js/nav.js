
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
