document.addEventListener('musickitloaded', function() {
  // MusicKit configuration starts //
  MusicKit.configure({
    developerToken: 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTSzlRQzdRVE4ifQ.eyJpYXQiOjE1MjgyNDE0MzEsImV4cCI6MTU0Mzc5MzQzMSwiaXNzIjoiVUM5REc5Mko2SiJ9.vAiX38WqbW_CAGr296-EQntZU8HcLq0MLg0f7P8i-STa9Oy5LgaTxbDCSlD9vZk2uzpJP6kRcH-YomqTmmLS9A',
	app: {
      name: 'Learn',
      build: '1.0'
    },
    declarativeMarkup: true
  });
  // MusicKit configuration ends //

  // Global variables
  var music = MusicKit.getInstance();
  var roomId = parseInt($("#roomId").text());
  var roomType = parseInt($("#roomType").text());
  var adminInterval;
  var normalInterval;
  var jumpInterval;

  // Decides user type, admin or normal
  if($('#startBtnAdmin').length){
    $('#startBtnAdmin').on('click', function(){
      startAdmin();
    })
  } else{
    $('#startBtnNormal').on('click', function(){
      startNormal();
    })
  }

  // Admin related starts //
  function startAdmin() {
    $.post("/songcloud/start_admin",{roomId:roomId, roomType:roomType})
    .done(function(data) {
      play(data.songId, data.time);
      $("#now-playing").text(data.message);
      updateCurPlaylist();
      adminInterval = setInterval(updateAdmin, 1000);
    })
    .fail(function() {
      alert("error");
    });
  }

  function updateAdmin() {
    updateLikeDislike();
    time = music.player.currentPlaybackTime;
    progress = music.player.currentPlaybackProgress;
    // update progress bar
    document.getElementById("progress").style.width = progress*100 + "%";
    // update time
    if(time < 10) {
      timeStr = "0:0" + time;
    }
    else {
      timeStr = "0:" + time;
    }
    $('#time').text(timeStr);
    // update song in DB and play next
    if(progress > 0.95) {
      clearInterval(adminInterval);
      updateSongDefault();
    }
    else {
      // update time of current song in DB
      updateTime(time);
    }
  }

  function updateTime(time) {
    var time = music.player.currentPlaybackTime; // latest, avoid race condition
    $.post("/songcloud/update_time",{roomId:roomId, time:time, roomType:roomType})
    .done(function(data) {
    })
  }

  function updateSongDefault() {
    $.post("/songcloud/update_song_default",{roomId:roomId, roomType:roomType})
    .done(function(data) {
      play(data.songId, data.time);
      $("#now-playing").text(data.message);
      updateCurPlaylist();
      adminInterval = setInterval(updateAdmin, 1000);
    })
    .fail(function() {
      alert("updateSongDefault error");
    });
  }
  // Admin related ends //

  // Normal related starts //
  function startNormal() {
    fetchCurrentSong();
  }

  function fetchCurrentSong() {
    $.post("/songcloud/fetch_current_song",{roomId:roomId, roomType:roomType})
    .done(function(data) {
      if(data.songId != 0) {
        play(data.songId, data.time);
        updateCurPlaylist();
        normalInterval = setInterval(updateNormal, 1000);
      }
      $("#now-playing").text(data.message);
    })
    .fail(function() {
      alert("error");
    });
  }

  function updateNormal() {
    updateLikeDislike();
    time = music.player.currentPlaybackTime;
    progress = music.player.currentPlaybackProgress;
    // update progress bar
    document.getElementById("progress").style.width = progress*100 + "%";
    // update time
    if(time < 10) {
      timeStr = "0:0" + time;
    }
    else {
      timeStr = "0:" + time;
    }
    $('#time').text(timeStr);
    // fetch next song
    if(progress > 0.95) {
      clearInterval(normalInterval);
      fetchCurrentSong();
    }

  }
  // Normal related ends //

  // Room playlist related starts //
  function updateCurPlaylist() {
    $.get("/songcloud/get_cur_playlist", {roomId:roomId, roomType:roomType})
    .done(function(data) {
      var list = $("#curPlaylist");
      list.html('');
      for(var i = 0; i < data.songs.length; i++) {
        var song = data.songs[i];
        // append
        console.log(song.info);
        var li = $("<li>", {class: 'list-group-item1 lightgrey'});
        li.append("<span>" + song.info + "</span>");
        var voteBtn = '<button class="badge">' +
        '<span class="vote"><i class="glyphicon glyphicon-heart-empty"></i></span>' +
        '<span class="count" id="countVote">' + song.vote +
        '</span></button>'
        li.append(voteBtn);
        list.append(li);
      }
    });
  }
  // Room playlist related ends //

// Like dislike related starts //
function updateLikeDislike() {
  $.post("/songcloud/get_like_dislike", {roomId:roomId, roomType:roomType})
  .done(function(data) {
    if(data == '') {
        return;
    }
    var dislike = data.countdislike;
    var count = $("#countdislike");
    var next = $("#next");
    var maxNum = Math.ceil(data.memberNum*0.6);
    if (dislike >= maxNum) {
      if($('#startBtnAdmin').length) {
        clearInterval(adminInterval);
        updateSongDefault();
        $("#like-button").on('click',addLike);
        $("#dislike-button").on('click',addDislike);
      }
      else {
        $("#like-button").on('click',addLike);
        $("#dislike-button").on('click',addDislike);
        jumpInterval = setInterval(FindNext, 1000);
      }
    }
    count.text(dislike);

    var like = data.countlike;
    var countlike = $("#countlike");
    countlike.text(like);
  })
}

  function FindNext() {
    $.post("/songcloud/fetch_current_song",{roomId:roomId, roomType:roomType})
    .done(function(data) {
      if(data.songId != 0) {
        if(data.message != $("#now-playing").text()) {
          play(data.songId, data.time);
          updateCurPlaylist();
          clearInterval(jumpInterval);
        }
      }
      $("#now-playing").text(data.message);
    })
    .fail(function() {
      alert("error");
    });
  }
// Like dislike related ends //

  function play(songId, time) {
    music.setQueue({
      songs: [songId]
    }).then(function() {
      music.player.play();
      music.player.seekToTime(time);
    });
  }



  $(document).ready(function () {
    $("#like-button").on('click',addLike);
    $("#dislike-button").on('click',addDislike);
});

function addDislike() {
  var countNum = $('#countdislike').text();
  var count = $("#countdislike");
  count.text(parseInt(countNum)+1);
  $("#dislike-button").off('click',addDislike);
  var roomId = parseInt($("#roomId").text());

  $.post("/songcloud/update_dislike",{roomId:roomId, roomType:roomType})
  .done(function(data) {
  })
}

function addLike() {
  var countNum = $('#countlike').text();
  var count = $("#countlike");
  count.text(parseInt(countNum)+1);
  $("#like-button").off('click',addLike);
  var roomId = parseInt($("#roomId").text());

  $.post("/songcloud/update_like", {roomId:roomId, roomType:roomType})
  .done(function(data) {
  })
}

});


