document.addEventListener('musickitloaded', function() {
  let music = MusicKit.getInstance();

  $("#searchBtn").click(function(){
    content = $("#searchContent").val();
    $("#searchContent").val(''); // clear search content
    $("#searchResult").empty(); // clear prev search result
    music.api.search(content, {limit:10})
    .then(function(result) {
      for (i = 0; i < 10; i++) {
        attr = result.songs.data[i].attributes;
        info = "<i>" + attr.name + "</i> BY " + attr.artistName;
        songId = result.songs.data[i].id;
        btnId = "song" + i.toString();
        param = songId+","+i.toString()+","+attr.name+
          ","+attr.artistName+",album"
        console.log(param);
        func = 'searchMusic("' + param + '")';
        button = "<button class='btn btn-warning col-md-2 center-block' onclick='" +
          func + "' id='" + btnId + "'>Add</button>"
        console.log(button);
        html = "<li class='list-group-item'><div class='row'><div class='col-md-9'><h4>" + info +
          "</h4></div>" + button + "</div></li>";
        $("#searchResult").append(html);
      }
    });
  });

});

function searchMusic(param) {
  var params = param.split(",");
  songId = params[0];
  btnId = "#song" + params[1];
  name = params[2];
  artist = params[3];
  album = params[4];
  id = $(helperId).text();
  type = $(helperType).text();
  console.log(type);

  $.post("/songcloud/add_music",
  {type:type, id:id, songId:songId, name:name, artist:artist, album:album})
  .done(function() {
    $(btnId).html("Added");
    $(btnId).prop('disabled', true); // disable button
  })
  .fail(function() {
    alert("error");
  });
}