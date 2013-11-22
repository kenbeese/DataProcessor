
function notice_api_result(res, st){
    var $notice = $("header>span");
    var exit_code = res["exit_code"];
    if(exit_code == 0){
        $notice.text("API call Success!");
    }else{
        $notice.text("API call fails: " + res["message"]);
    }
}

function enable_edit(){
    enable_comment_edit();
}

function send_comment(comment, path){
    $.post("/cgi-bin/api.cgi",
        {
            "type": "pipe",
            "name": "add_comment",
            "args": JSON.stringify([comment, path])
        }, notice_api_result, "json"
    );
}

function enable_comment_edit(){
    $("td.comment").off("click");
    $("td.comment").bind("click", function(event){
        var comment = this.innerHTML;
        var path = $(this).parent().attr("path");
        $(this).replaceWith(
            $("<input>")
                .addClass("comment")
                .attr("value", comment)
                .attr("path", path)
            );
        enable_comment_input();
    });
}

function enable_comment_input(){
    $("input.comment").off("click");
    $("input.comment").bind("blur", function(event){
        var comment = this.value;
        var path = $(this).parent().attr("path");
        send_comment(comment, path)
        $(this).replaceWith(
            $("<td>")
                .addClass("comment")
                .text(comment)
                .attr("path", path)
            );
        enable_comment_edit();
    })
}

function widget_html(title, widgets){
    var $widget_html = $("<div>").addClass("Widget");
    $("<h2>")
        .addClass("WidgetTitle")
        .text(title)
        .appendTo($widget_html);

    for(var i=0; i<widgets.length; i++){
        $(widgets[i])
            .addClass("WidgetBody")
            .appendTo($widget_html);
    }
    return $widget_html
}

function enable_name_link(){
    $("td.name").off("click");
    $("td.name").bind("click", function(event){
        var name = this.innerHTML;
        var path = $(this).parent().attr("path");
        $.getJSON("/cgi-bin/body.cgi",
            {
                "type": "Widgets",
                "path": path,
                "table_type": "children"
            }, function(widgets){
                var $widget_html = widget_html(name, widgets);
                $("section#Widgets").append($widget_html);
                enable_name_link();
                enable_edit();
            });
    });
}

