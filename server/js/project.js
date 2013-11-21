function enable_Project_comment_edit(){
    $("nav#Projects td.comment").bind("click", function(event){
        var txt = this.innerHTML;
        var path = $(this).attr("path");
        $(this).replaceWith(
            $("<input>")
                .addClass("comment")
                .attr("value", txt)
                .attr("path", path)
            );
        enable_Project_comment_input();
    });
}

function enable_Project_comment_input(){
    $("nav#Projects input.comment").bind("blur", function(event){
        var txt = this.value;
        var path = $(this).attr("path");
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
        enable_Project_comment_edit();
    })
}

function enable_Project_name_link(){
    $("nav#Projects td.name").bind("click", function(event){
        var name = this.innerHTML;
        var path = $(this).attr("path");
        $("section#Widgets").empty().append($("<h2>").text(name));
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
                enable_Table();
            });
    });
}

function ready_Projects(){
    $("nav#Projects").append(
        $("<table>").append($("<thead>")).append($("<tbody>"))
    );
    $.getJSON("/cgi-bin/body.cgi", {"type": "Projects"},
        function(res){
            var keys = res["keys"]
            var table = res["table"]

            /* Header */
            keys = keys;
            var $thead = $("<tr>");
            for(var i=0; i<keys.length; i++){
                if(keys[i] == "path"){
                    continue;
                }
                $thead.append($("<th>").text(keys[i]));
            }
            $("nav#Projects>table>thead").append($thead);

            /* Body */
            for(var n=0; n<table.length; n++){
                var $tbody = $("<tr>");
                var path = table[n]["path"];
                for(var i=0; i<keys.length; i++){
                    if(keys[i] == "path"){
                        continue;
                    }
                    var $td = $("<td>").text(table[n][keys[i]]).attr("path", path);
                    $td.addClass(keys[i]);
                    $tbody.append($td);
                }
                $("nav#Projects>table>tbody").append($tbody);
            }
            enable_Project_comment_edit();
            enable_Project_name_link();
        });
}

$(function(){
    ready_Projects();
});
