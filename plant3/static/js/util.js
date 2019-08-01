/**
 * Created by richkl on 7/18/2016.
 */

var mytime = 0;

// async true to execute async calls, false for sync calls
function callGetAJAX(retFunc, async, target) {
    var xhttp = new XMLHttpRequest();

    if ( async ) {
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4) {
                retFunc.apply(this, [xhttp.status, xhttp.responseText]);
            }
        };
    };

    xhttp.open("GET", target, async);
    xhttp.send();

    if ( !async ) {
        return xhttp.responseText;
    }
}

// async true to execute async calls, false for sync calls
function callGetAJAXExtra(retFunc, async, target, param1, param2) {
    var xhttp = new XMLHttpRequest();

    if ( async ) {
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 ) {
                retFunc.apply(this, [param1, param2, xhttp.status, xhttp.responseText]);
            }
        };
    };

    xhttp.open("GET", target, async);
    xhttp.send();

    if ( !async ) {
        return xhttp.responseText;
    }
}

function callPostAJAX(retFunc, async, target, formdata) {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 ) {
            retFunc.apply(this, [xhttp.status, xhttp.responseText ]);
        }
    };

    xhttp.open("POST", target, async);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(formdata);
}

function callPostAJAXExtra(retFunc, async, target, formdata, param1, param2) {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 ) {
            retFunc.apply(this, [param1, param2, xhttp.status, xhttp.responseText ]);
        }
    };

    xhttp.open("POST", target, async);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(formdata);
}

function onclickScroll() {
    var text = document.getElementById("scrollbutton").innerHTML;
    if ( text.indexOf("More...") != -1 ) {
        window.scrollTo(0, document.body.scrollHeight - 50);
        document.getElementById("scrollbutton").innerHTML = "Less...";
    }
    else {
        window.scrollTo(0, 0);
        document.getElementById("scrollbutton").innerHTML = "More..."
    }
}


