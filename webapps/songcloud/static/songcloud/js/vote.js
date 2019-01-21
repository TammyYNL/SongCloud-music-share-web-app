$(document).ready(function () {
    $("#like-button").click(addLike);
    $("#dislike-button").click(addDislike);

});

function addDislike() {
  var countNum = $('#countdislike').text();
  var count = $("#countdislike");
  count.text(parseInt(countNum)+1);
  $("#dislike-button").unbind();
  var roomId = parseInt($("#roomId").text());

  $.post("/songcloud/update_dislike",{roomId:roomId})
  .done(function(data) {
  })
  .fail(function() {
    alert("addDislike error");
  });
}

function addLike() {
  var countNum = $('#countlike').text();
  var count = $("#countlike");
  count.text(parseInt(countNum)+1);
  $("#like-button").unbind();
  var roomId = parseInt($("#roomId").text());

  $.post("/songcloud/update_like", {roomId:roomId})
  .done(function(data) {
  })
  .fail(function (data, status) {
    alert("addLike fail");
  });
}