$(function(){
    $("nav#Manip")
        .append($("<textarea>").attr("placeholder", "manipulation").attr("rows", 0))
        .append($("<button>").text("execute"))
        .append("<span>");
    $("nav#Manip>button").bind("click", function(event){
        var manip_json = this.previousSibling.value;
        $(this).siblings("span").text("sending...");
        $.post("/cgi-bin/api.cgi", 
            {
                "type": "manip",
                "manip": manip_json
            },
            function(res, st){
                notice_api_result(res, st);
            }, "json");
    });
});
