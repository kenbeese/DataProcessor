
$(function(){
    $("nav#ManipJSON")
        .append("<textarea>")
        .append($("<button>").text("execute"))
        .append("<span>");
    $("nav#ManipJSON>button").bind("click", function(event){
        var manip_json = this.previousSibling.value;
        $(this).siblings("span").text("sending...");
        $.post("/cgi-bin/api.cgi", 
            {
                "type": "manip",
                "manip": manip_json
            },
            function(res, st){
                var $result = $("nav#ManipJSON>span");
                var exit_code = res["exit_code"];
                if(exit_code == 0){
                    $result.text("Success!");
                }else{
                    $result.text("Error: " + res["message"]);
                }
            }, "json");
    });
});
