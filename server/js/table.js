/**
 * send comment to server
 */
function send_comment(comment, path){
    $.post("/cgi-bin/api.cgi",
        {
            "type": "pipe",
            "name": "add_comment",
            "args": JSON.stringify([comment, path])
        }, notice_api_result, "json"
    );
}


/**
 * generate a wedget <div/> in section#Widgets
 */
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

/**
 * ready table 
 */
function ready_table(){
    $("tbody>tr")
        .off("click", "td.name")
        .off("click", "td.comment")
        .off("blur", "input.comment");
    $("tbody>tr")
        .on("click", "td.name", function(event){
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
                    ready_table();
                });
        })
        .on("click", "td.comment", function(event){
            var comment = this.innerHTML;
            var path = $(this).parent().attr("path");
            $(this).replaceWith(
                $("<input>")
                    .addClass("comment")
                    .attr("value", comment)
                    .attr("path", path)
                );
        })
        .on("blur", "input.comment", function(event){
            var comment = this.value;
            var path = $(this).parent().attr("path");
            send_comment(comment, path)
            $(this).replaceWith(
                $("<td>")
                    .addClass("comment")
                    .text(comment)
                    .attr("path", path)
                );
        });
}
