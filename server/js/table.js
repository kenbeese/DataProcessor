
function enable_Table_comment_edit(){
    $("section#Widgets td.comment").bind("click", function(event){
        var txt = this.innerHTML;
        var path = $(this).parent().attr("path");
        $(this).replaceWith(
            $("<input>")
                .addClass("comment")
                .attr("value", txt)
                .attr("path", path)
            );
        enable_Table_comment_input();
    });
}

function enable_Table_comment_input(){
    $("section#Widgets input.comment").bind("blur", function(event){
        var txt = this.value;
        var path = $(this).parent().attr("path");
        $.post("/cgi-bin/api.cgi",
            {
                "type": "pipe",
                "name": "add_comment",
                "args": JSON.stringify([txt, path])
            }, notice_api_result, "json"
        );
        $(this).replaceWith(
            $("<td>")
                .addClass("comment")
                .text(txt)
                .attr("path", path)
            );
        enable_Table_comment_edit();
    })
}

function enable_Table_name_link(){
    $("section#Widgets td.name").bind("click", function(event){
        var name = this.innerHTML;
        var path = $(this).parent().attr("path");
        $("section#Widgets").append($("<h2>").text(name));
        $.getJSON("/cgi-bin/body.cgi",
            {
                "type": "Widgets",
                "path": path,
                "table_type": "children"
            }, function(widgets){
                var $WidgetSec = $("section#Widgets");
                for(var i=0; i<widgets.length; i++){
                    $("section#Widgets").append($(widgets[i]))
                }
                enable_Table_comment_edit();
            });
    });
}

function enable_Table(){
    enable_Table_comment_edit();
    enable_Table_name_link();
}

$(function(){
});
