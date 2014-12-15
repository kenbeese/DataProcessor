var api_url = "/cgi-bin/api.cgi"

$(function(){
  $.post(api_url, {
      "type": "pipe", 
      "name": "projects_html",
      "args": "[]", 
    }, function (res) {
      paths = res["paths"];
      html = res["html"];
      $("#ProjectList").append(html);
      $.each(paths, function(i, path){
        $.post(api_url, {
            "type": "pipe",
            "name": "project_table_html",
            "args": JSON.stringify([path,])
        }, function(res){
          $("#Projects").append(res);
        });
      });
    }
  );
})
