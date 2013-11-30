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
    $("section, nav#Projects")
        .off("click", "table>tbody>tr>td.name")
        .off("click", "table>tbody>tr>td.comment")
        .off("blur", "table>tbody>tr>input.comment");
    $("section, nav#Projects")
        .on("click", "table>tbody>tr>td.name", function(event){
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
        .on("click", "table>tbody>tr>td.comment", function(event){
            var comment = this.innerHTML;
            var path = $(this).parent().attr("path");
            $(this).replaceWith(
                $("<input>")
                    .addClass("comment")
                    .attr("value", comment)
                    .attr("path", path)
                );
        })
        .on("blur", "table>tbody>tr>input.comment", function(event){
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

/**
 * Sort table
 */
    var sortOrder = 1;
    $("section").off("click", "div.Widget>table>thead>tr.items>th");
    $("section").on("click", "div.Widget>table>thead>tr.items>th",
                    function(){
                        // get tbody
                        var $rows = $(this).parents("table").children("tbody").find("tr");
                        var col = $(this).index();

                        // Sort
                        $rows.sort(function(a, b){
                            return compare(a, b, col) * sortOrder;
                        });
                        $(this).parents("table").children("tbody")
                            .empty().append($rows);

                        // update mark of sort order
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
        if (isNaN(parseFloat(_a))) {
            // var __a = _a.toLowerCase();
            // var __b = _b.toLowerCase();
            var __a = _a;
            var __b = _b;
            if (__a < __b) //sort string ascending
                return -1;
            if (__a > __b)
                return 1;
            return 0; //default return value (no sorting)
        } else {
            var __a = parseFloat(_a);
            var __b = parseFloat(_b);
            return (__a - __b);
        }
    };
}
