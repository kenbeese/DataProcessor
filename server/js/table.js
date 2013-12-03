function correct_width_table($table_object){
    /** correct table width
     *
     *  +-------+----+    +-------+----+    +-------+
     *  |  G1   | G2 |    |  G1   | G2 |    |G1 | G2|
     *  +---+---+----+ >> +---+---+----+ >> +---+---+
     *  | a | b | c  |    | a | c |    |    | a | c |
     *  +---+---+----+    +---+---+----+    +---+---+
     *                 ^^                ^^
     *               by others       this function
     */
    var $groups = $table_object.find("thead>tr.group>th");
    // create group name list
    var group_list = [];
    $groups.each(function(){
        group_list.push($(this).data("group"));
    });
    // count group number
    var group_num = {};
    for (var i in group_list){
        group_num[group_list[i]] = 0;
    }
    // count each group number
    $table_object.parent().find("div.tableMenu div>span.item").each(function(){
        if ($(this).hasClass("show")) {
            for (var j in group_list){
                if ($(this).data("group") == group_list[j]){
                    group_num[group_list[j]] += 1;
                    break;
                }}}
    });
    // correct width of table.
    $groups.each(function(){
        $(this).attr("colspan", group_num[$(this).data("group")]);
        if (group_num[$(this).data("group")] == 0){
            $(this).hide();
        } else {
            $(this).show();
        }});
}

function add_menu($widget_html){

    // create hide and show checkbox
    var $items = $widget_html.find("table.childrenTableWidget>thead>tr.items>th");
    var $div_check = $("<div>").addClass("tableMenu");
    var previous_group = "";
    var $group;
    /* create following group blocks
     <div>
     <span class="group" show=1 group="group1">group1</span>:
     <span class="item" show=? group="group1">item1</span>
     <span class="item" show=? group="group1">item2</span>
     </div>
     */
    $items.each(function (){
        // read item name and group name from table header.
        var now_item = $(this).attr("class");
        var group = $(this).data("group");
        // create next group
        if (group != previous_group){
            $div_check.append($group);
            $group = $("<div>").text(": ");
            var $span = $("<span>").text(group).addClass("group").addClass("show").data("group", group);
            $group.prepend($span);
        }
        // read coockie data
        var show = $.cookie($(this).parents("table").attr("path") + "-" +
                            group + "-" + now_item + "-show");
        if (show == undefined) {
            show = 1;
            $.cookie($(this).parents("table").attr("path") + "-" +
                     group + "-" + now_item + "-show", show);
        }
        // set visible state
        $span = $("<span>").text(now_item).addClass("item");
        $span.data("item", now_item).data("group", group);
        if (show == "1") {
            $span.addClass("show");
        }
        $group.append($span);
        $group.append($("<span>").text(" "));
        // for next group
        previous_group = group;
    });
    $div_check.append($group);
    $widget_html.find("table.childrenTableWidget").before($div_check);
    // hide previously hidden item.
    $widget_html.find("div.tableMenu span.item").each( function(){
        if (! $(this).hasClass("show")){
            var selector = "table th." + $(this).data("item") +
                    ", table td." + $(this).data("item");
            $(this).parents("div.Widget").find(selector).hide();
        }});
    correct_width_table($widget_html.find("table.childrenTableWidget"));
}

function enable_name_link($wrap_table){
    /** enable link on name table data
     *
     * Parameters
     * ----------
     * wrap_table : wrap set including tables
     */
    $wrap_table
        .off("click", "table>tbody>tr>td.name")
        .on("click", "table>tbody>tr>td.name", function(event){
            var name = this.innerHTML;
            var path = $(this).parent().attr("path");
            get_widgets(path, function($widget){
                add_widget(name, $widget);
                ready_table();
            });
        });
}

function enable_editable_comment($wrap_table){
    /** enable editable comment
     *
     * Parameters
     * ----------
     * wrap_table : wrap set including tables
     */
    $wrap_table
        .off("click", "table>tbody>tr>td.comment")
        .on("click", "table>tbody>tr>td.comment", function(event){
            var comment = this.innerHTML;
            var path = $(this).parent().attr("path");
            var $parent = $(this).parent();
            $(this).replaceWith(
                $("<input>")
                    .addClass("comment")
                    .attr("value", comment)
                    .attr("path", path)
                );
            $parent.find("input.comment").focus();
        })
        .off("blur", "table>tbody>tr>input.comment")
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
}

function enable_sort($wrap_table){
    /** enable sort
     *
     * Parameters
     * ----------
     * wrap_table : wrap set including tables
     */
    var sortOrder = 1;
    $("section")
        .off("click", "table>thead>tr.items>th")
        .on("click", "table>thead>tr.items>th", function(){
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
}

function enable_show_hide($wrap_table){
    /** Hide or Show table Item
     *
     * Parameters
     * ----------
     * wrap_table : wrap set including tables
     */
    $wrap_table
        .off("click", "div.tableMenu>div>span.item")
        .on("click", "div.tableMenu>div>span.item", function(){
            var now_item = $(this).data("item");
            var selector = "table th." + now_item +
                    ", table td." + now_item;
            if ($(this).hasClass("show")){
                $(this).parents("div.Widget").find(selector).hide();
                $(this).removeClass("show");
                $.cookie($(this).parents("div.Widget").find("table").attr("path") + "-" +
                         $(this).data("group") + "-" + now_item + "-show", 0);
            } else {
                $(this).parents("div.Widget").find(selector).show();
                $(this).addClass("show");
                $.cookie($(this).parents("div.Widget").find("table").attr("path") + "-" +
                         $(this).data("group") + "-" + now_item + "-show", 1);
            }
            correct_width_table($(this).parents("div.Widget")
                                .find("table.childrenTableWidget"));
        })
        .off("click", "div.tableMenu>div>span.group")
        .on("click", "div.tableMenu>div>span.group", function(){
            var now_group = $(this).data("group");
            var selector = "table th[data-group=" + now_group + "]" +
                    ", table td[data-group=" + now_group + "]";
            if ($(this).hasClass("show")){
                $(this).siblings().removeClass("show");
                $(this).siblings().each(function(){
                    $.cookie($(this).parents("div.Widget").find("table").attr("path") + "-" +
                             $(this).data("group") + "-" +
                             $(this).data("item") + "-show", 0);
                });
                $(this).removeClass("show");
                $(this).parents("div.Widget").find(selector).hide();
            } else {
                $(this).siblings().addClass("show");
                $(this).siblings().filter(".item").each(function(){
                    $.cookie($(this).parents("div.Widget").find("table").attr("path") + "-" +
                             $(this).data("group") + "-" +
                             $(this).data("item") + "-show", 1);
                });
                $(this).addClass("show");
                $(this).parents("div.Widget").find(selector).show();
            }
            correct_width_table($(this).parents("div.Widget").find("table.childrenTableWidget"));
        });
}

function ready_table_common($wrap_table){
    enable_name_link($wrap_table);
    enable_editable_comment($wrap_table);
}

function ready_table_all($wrap_table){
    add_menu($wrap_table);
    enable_name_link($wrap_table);
    enable_editable_comment($wrap_table);
    enable_sort($wrap_table);
    enable_show_hide($wrap_table);
}
