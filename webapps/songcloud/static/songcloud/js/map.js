$(document).ready(function ($) {
    $("#search-real-room-button").click(searchRealRoom);
    $("#locate-button").click(Locate);

//  // Periodically refresh to-do list
//  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

//  function csrfSafeMethod(method) {
//    // these HTTP methods do not require CSRF protection
//    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

});


  var map, infoWindow, marker;
  function Locate() {
   infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = { //latlng
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

       $("#latitude").val(position.coords.latitude);
        $("#longtitude").val(position.coords.longitude);

        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'location': pos}, function(results, status) {
        if (status === 'OK') {
          if (results[0]) {
           infoWindow.setContent(results[0].formatted_address);
            $("#location").val(infoWindow.getContent())

          } else {
            window.alert('No results found');
          }
        } else {
          window.alert('Geocoder failed due to: ' + status);
        }
      });
      });
    }
  }


  function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 39.605, lng: -80.76},
      zoom: 17
    });
    infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = { //latlng
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'location': pos}, function(results, status) {
        if (status === 'OK') {
          if (results[0]) {
            marker = new google.maps.Marker({
              position: pos,
              map: map
            });

            attachMessage(marker, "you are here: "+results[0].formatted_address)
            infoWindow.setContent(results[0].formatted_address);
            infoWindow.open(map, marker);

          } else {
            window.alert('No results found');
          }
        } else {
          window.alert('Geocoder failed due to: ' + status);
        }
      });

        map.setCenter(pos);
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  }

  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
  }

  function searchRealRoom() {
    $.post("/songcloud/enter_realroom")
      .done(function(data) {
          initMap();

          for (var i = 0; i < data.real_rooms.length; i++) {
            var pos = {
              lat: data.real_rooms[i].latitude,
              lng: data.real_rooms[i].longtitude
            };

            var marker_room = new google.maps.Marker({position: pos, map:map});
            attachMessage(marker_room, data.real_rooms[i].name);
            attachHtml(marker_room, data.real_rooms[i], )
          }
      })
      .fail(function (data, status) {
    alert('fail ' + data.status + 'reason' + status);
    });

  }

  function attachMessage(marker, content) {
        var infowindow_room = new google.maps.InfoWindow({
          content: content
        });

        marker.addListener('click', function() {
          infowindow_room.open(marker.get('map'), marker);
        });
      }

  function attachHtml(marker2, real_room) {
    marker2.addListener('click', function() {
    var pos = { //latlng
          lat: real_room.latitude,
          lng: real_room.longtitude
        };

    var path = [marker.getPosition(), marker2.getPosition()];
    var heading = Math.abs(google.maps.geometry.spherical.computeHeading(path[0], path[1]).toFixed(1));
//    console.log(heading);


        $("#real-room-name").text("").append(real_room.name);
        $("#real-room-introduction").text("").append(real_room.description);
        $("#real-room-distance").text("").append(heading + "m");
//        $("#real-room-distance").val(heading);
        $('#joinBtn').off('click');
        $("#joinBtn").click(function(){
            if (heading > 500) {
                alert("You cannot enter this room since you're non't near the room！");
            } else {
                window.location = window.location.origin+"/songcloud/real_room/"+real_room.id;
            }
        });



        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'location': pos}, function(results, status) {
        if (status === 'OK') {
          if (results[0]) {
            $("#real-room-location").text("").append(results[0].formatted_address);
          } else {
            window.alert('No results found');
          }
        } else {
          window.alert('Geocoder failed due to: ' + status);
        }
      });
        map.setCenter(pos);
    });
  }
