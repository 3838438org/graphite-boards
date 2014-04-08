serialize = function(obj) {
  var str = [];
  for(var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&")
}

// Make sure we resize graphs as the window size changes.
var resizing = false

$( window ).resize(function() {
    if (resizing == false) {
        resizing = true
        id = setTimeout(doneResizing, 1000);
    }
});

function doneResizing() {
    resizing = false
    location.reload()
}

function query_to_params(query) {
        var targets = []
        var vars = [], hash
        var varmap = []
        var hashes = query.slice(query.indexOf('?') + 1).split('&');

    for(var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=')
        vars.push(hash[0])
        if(hash[0] == 'target') {
            targets.push(hash[1])
        } else {
            varmap[hash[0]] = hash[1]
        }
    }
    varmap['target'] = targets.join('&target=');
    return varmap
}

function calcAllGraphDimensions() {
    gridster.$widgets.each($.proxy(function(i, widget) {
        calcGraphDimensions(widget)
    }));
}

// Recaclulates the correct width of a graph by taking the width of its parent div.
function calcGraphDimensions(widget) {
        var graph_image = $(widget)[0].children[0]
        var url = graph_image.parentNode.dataset.imgsrc.split("?")[0];
        var params = query_to_params(graph_image.parentNode.dataset.imgsrc)
        params['height'] = parseInt(window.getComputedStyle(graph_image.parentNode).height.split('px')[0]);
        params['width'] = parseInt(window.getComputedStyle(graph_image.parentNode).width.split('px')[0]);
        if (graph_image.parentNode.dataset.friendlyname != '') {
          params['title'] = graph_image.parentNode.dataset.friendlyname
        }

        graph_image.parentNode.dataset.imgsrc = (url + '?' + decodeURIComponent(serialize(params)))
        loadImage(widget)
}

function loadImage(widget) {
    console.log(widget.dataset.imgsrc)
        widget.children[0].src = widget.dataset.imgsrc
        $(widget).removeClass('not-loaded')
}

// Cycles through all the IMG elements on the page and reloads them every
// 30 seconds
function reloadGraphs() {
    $('img').each(function(idx, value) {
        var url = $(this).attr('src').split("?")[0];
        var params = query_to_params($(this).attr('src'))
        params['time-stamp'] = new Date().getTime()
        $(this).attr('src', url + '?' + decodeURIComponent(serialize(params)))
    });
    setTimeout("reloadGraphs()", 30000)
}

function sendUpdate() {
    msg_object = {}
    layout_object = {}
    dashboard_id = window.location.pathname.split("/")[2]


    gridster.$widgets.each($.proxy(function(i, widget) {
      graph_object = {
        row: $(widget).coords().grid.row,
        col: $(widget).coords().grid.col,
        size_x: $(widget).coords().grid.size_x,
        size_y: $(widget).coords().grid.size_y
      }
      layout_object[$(widget).data('id')] = graph_object
    }));

    console.log(layout_object)
    msg_object[dashboard_id] = layout_object

    $.ajax({
      url: '/update/layout',
      contentType: "application/json",
      type: 'PUT',
      data: JSON.stringify(msg_object),
      success: function(data) {
        console.log('Sent: ' + JSON.stringify(msg_object));
      }
    });

}
