var view_map;
var bounds;
var markers = []

String.prototype.format = function () {
	var args = arguments;
	return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
		if (m == "{{") { return "{"; }
		if (m == "}}") { return "}"; }
		return args[n];
	});
};

function addAddress() {
			$('.preloader-wrapper').show();
		console.log("Button clicked")
			var curr_address = document.getElementById("autocomplete").value
			$('#address').val('');
			$.getJSON("/addLocation", {
				curr_address: curr_address,
			}, function(response) {
				var html = "<li class='collection-item' id='{0}'>"
				+"{0} <a href='#' id='removeLocation' class='secondary-content'><i class='material-icons'>remove_circle</i></a></li>"
				$(html.format(curr_address)).hide().prependTo('#location_list').slideDown('slow');

				updateDynamicMap(response, curr_address)
				document.getElementById('autocomplete').value='';
			$('.preloader-wrapper').hide('slow');

			});
}

function loadAddress(curr_address) {
	console.log("Loading addresses")
			$('.preloader-wrapper').show();

	$.getJSON("/loadLocation", {
				curr_address: curr_address,
			}, function(response) {
				var html = "<li class='collection-item' id='{0}'>"
				+"{0} <a href='#' id='removeLocation' class='secondary-content'><i class='material-icons'>remove_circle</i></a></li>"
				    $(html.format(curr_address)).hide().prependTo('#location_list').slideDown('slow');
				updateDynamicMap(response, curr_address)
			$('.preloader-wrapper').hide('slow');

			});
}

$(function () {
  $(document).scroll(function () {
    var $nav = $(".nav-wrapper");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });
});
	$(document).ready(function() {
		$(".button-collapse").sideNav();
		$('select').material_select();
		$('.modal').modal();

		$('#removeLocation').on('click', function(event) {
			console.log("Removing location")
			// $(this).parent().remove();
			$(this).parent().hide('slow', function() {
				$(this).remove(); 
			});

			curr_address = $(this).parent().attr('id')
			$.getJSON("/removeLocation",  {
				curr_address: curr_address,
			});
		});

		$('#add_address').on('click', function(event) {
			addAddress()

		});

		$('#join_session').on('click', function(event) {
			var session_id = document.getElementById("session_id").value
			window.location.replace(session_id);

		});


		$(document).keypress(function(e) {
			if(e.which == 13) {
				addAddress();
			}
		});

		var concurrentUpdate = function(data) {
			var session_info = $('#session').data();
			console.log(session_info)
			console.log(data)
			$('#location_list').prepend("<li class='collection-item'>" + data +" </li>");

		}
	
	});

	$(document).ajaxComplete(function () {
		$('#removeLocation').on('click', function(event) {
				console.log("Removing location")
			curr_address = $(this).parent().attr('id')
			$(this).parent().hide('slow');
			//$(this).parent().remove(); 
			
			$.getJSON("/removeLocation",  {
				curr_address: curr_address,
			});

			for (var i = 0; i < markers.length; i++) {
				if (markers[i].title == curr_address) {
					markers[i].setMap(null)
				}
			}



		});
	});

	function dynamicMap() {
		bounds = new google.maps.LatLngBounds();
        view_map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -33.8688197, lng: 151.2092955},
          zoom: 12,
         disableDefaultUI: true

        });

        map = new google.maps.Map(document.getElementById('background-map'), {
          center: {lat: -33.8688197, lng: 151.2092955},
          zoom: 8,
          streetViewControl: false,
          disableDefaultUI: true,
          draggable: true,
          scaleControl: false
        });
        initAutocomplete();
	}

	function updateDynamicMap(coords, curr_address) {
		console.log(coords)
		var marker = new google.maps.Marker({
			position:coords[0],
			animation: google.maps.Animation.DROP,
			title: curr_address
		})
		markers.push(marker)
		bounds.extend(marker.position);
		map.fitBounds(bounds);

		marker.setMap(view_map)
		view_map.setCenter(coords[0]);
		console.log(markers)
	}

// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

var placeSearch, autocomplete;
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

function initAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
      {types: ['geocode']});

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  // autocomplete.addListener('place_changed', fillInAddress);
}


// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}

	// function updateDynamicMap(coords) {
	// 		console.log(coords)
	// 	var map;
 //        map = new google.maps.Map(document.getElementById('map'), {
 //          center: {lat: coords[0]['lat'], lng: coords[0]['lng']},
 //          zoom: 15
 //        });
	// }