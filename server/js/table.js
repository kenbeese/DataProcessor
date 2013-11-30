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
    $("<button>")
        .text("hide")
        .bind("click", function(event){
            $(this).parent().remove();
        })
        .appendTo($widget_html);

    for(var i=0; i<widgets.length; i++){
        $(widgets[i])
            .addClass("WidgetBody")
            .appendTo($widget_html);
    }
    return $widget_html;
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
            send_comment(comment, path);
            $(this).replaceWith(
                $("<td>")
                    .addClass("comment")
                    .text(comment)
                    .attr("path", path)
                );
        });

    // Sort
    var sortOrder = 1;
    $("div.Widget>table>thead>tr.items").off("click", "th");
    $("div.Widget>table>thead>tr.items")
        .on("click", "th", function(){
            var $rows = $(this).parents("table").children("tbody").find("tr");
            var col = $(this).index();
            console.log(col);
            $rows.sort(function(a, b){
                return compare(a, b, col) * sortOrder;
            });

            $(this).parents("table").children("tbody")
                .empty().append($rows);

            // mark sort order
            var arrow = sortOrder === 1 ? "▲" : "▼";
            $(this).parent().find('span').remove();
            var span = $('<span>');
            $(this).prepend(span);
            $(this).find('span').text(arrow);

            // change sort order
            sortOrder *= - 1;
        });
    function compare(a, b, col) {
        var _a = $(a).find('td').eq(col).text();
        var _b = $(b).find('td').eq(col).text();
        return (_a * 1 - _b * 1);
    }};
