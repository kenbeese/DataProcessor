
function notice_api_result(res, st){
    /** show the result of API */
    var $notice = $("header>span");
    var exit_code = res["exit_code"];
    if(exit_code != 0){
        $notice
            .text("API call fails: " + res["message"])
            .css("color", "red");
    }
}

function send_comment(comment, path){
    /** send comment to server */
    $.post("/cgi-bin/api.cgi",
        {
            "type": "pipe",
            "name": "add_comment",
            "args": JSON.stringify([comment, path])
        }, notice_api_result, "json"
    );
}

function compare(a, b, col) {
    /** compare values
     *
     * Parameters
     * ----------
     *  a, b : <tr>
     *  col : int
     *      column number
     */
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
