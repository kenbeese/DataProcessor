$(function(){
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
                var path = table[n]["path"];
                var $tbody = $("<tr>").attr("path", path);
                for(var i=0; i<keys.length; i++){
                    var key = keys[i];
                    if(key == "path"){
                        continue;
                    }
                    var $td = $("<td>").text(table[n][key]);
                    $td.addClass(key);
                    $tbody.append($td);
                }
                $("nav#Projects>table>tbody").append($tbody);
            }
            enable_edit();
            enable_name_link();
        });
});
