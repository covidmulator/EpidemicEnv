function reset_log() {
  var target = $('#qlearning');
  target.empty();
}

function log(msg) {
  var target = $('#Log');
  var p = $('<p></p>');
  p.append(msg);
  target.append(p);
}

function print_map(s) {
  var string = s;
  var tbl = $('<table></table>');
  for (var y = 0; y < 4 ; ++y) {
    var tr = $('<tr></tr>');
    for (var x = 0; x < 6; ++x) {
      var thing = string.charAt(y * 6 + x);
      var item = null;
      if (thing == 0) item = $('<div style="width:20px;height:20px;background:white;">');
      else if (thing == 1) item = $('<img style="width:20px;height:20px;background:green;">');
      else if (thing == 2) item = $('<img style="width:20px;height:20px;background:purple;">');
      else if (thing == 3) item = $('<img style="width:20px;height:20px;background:blue;">');
      var td = $('<td style="width:20px;height:20px;border:2px solid;"></td>');
      if (item) td.append(item);
      tr.append(td);
    }
    tbl.append(tr);
  }
  log(tbl);
}

$(function() {
  var fn = Run;
  setInterval(fn, 100);
});

var counter = -1;

function Run() {
  reset_log();
  counter++
}
