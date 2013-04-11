
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
    /* generate table */
    $('<tr>',{
        id : "DataHeader"
    }).appendTo("table#DataTable>thead")
    $("tr#DataHeader")
        .append($("<th>").text("name"))
        .append($("<th>").text("date"));
    for(var i=0;i<confs.length;++i){
        $("tr#DataHeader").append($("<th>").text(confs[i]));
    }
}
