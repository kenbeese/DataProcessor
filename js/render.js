
function append_to_table_body($tr,l,d){
    for(var ci=0;ci<l.length;++ci){
        var com = l[ci];
        if(com in d){
            $tr.append($("<td>").text(d[com]));
        }else{
            $tr.append("<td>");
        }
    }
}

function append_to_table_header($tr,l){
    for(var ci=0;ci<l.length;++ci){
        $tr.append($("<th>").text(l[ci]));
    }
}

function render(data){
    var N = data.length;
    var confs = [];
    for(var i=0;i<N;++i){
        conf = data[i]["configure"];
        for(var c in conf){
            if(!(c in confs)){
                confs.push(c);
            }
        }
    }
    var pre_meta = ["name","date"];
    var post_meta = ["tags","comment"];
    var $head_tr = $('<tr>');
    append_to_table_header($head_tr,pre_meta);
    append_to_table_header($head_tr,confs);
    append_to_table_header($head_tr,post_meta);
    $head_tr.appendTo("table#DataTable>thead");
    for(var i=0;i<N;++i){
        var d = data[i];
        var $tr = $("<tr>");
        append_to_table_body($tr,pre_meta,d["meta"]);
        append_to_table_body($tr,confs,d["configure"]);
        append_to_table_body($tr,post_meta,d["meta"]);
        $tr.appendTo("table#DataTable>tbody");
    }
}
