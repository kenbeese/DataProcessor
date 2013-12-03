
function ready_widgets(){
    ready_table();
    // ready_figure()
}

function get_widgets(path, callback_f){ // TODO callback_table, callback_figure
    $.getJSON("/cgi-bin/body.cgi",
        {
            "type": "Widgets",
            "path": path,
            "table_type": "children"
        }, function(widgets){
            for(var i=0; i<widgets.length; i++){
                // TODO switch by widget type (table, figure)
                var $widget = $(widgets[i]);
                callback_f($widget);
            }
        });
}

function add_widget(title, $widget_inner_html){
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
    return $widget_html.append($widget_inner_html)
                       .appendTo("section#Widgets")
}

