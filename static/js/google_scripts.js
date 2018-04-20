	var map;
	var infowindow;
	var bounds;

	function initMap(convergence) {
		console.log("Initialising map")

        var convergence  = {lat: latitude, lng: longitude};
		// var convergence  = {lat: latitude , lng: longitude};
		map = new google.maps.Map(document.getElementById('map'), {
			center: convergence ,
			zoom: 15
		});

		background_map = new google.maps.Map(document.getElementById('background-map'), {
			center: convergence ,
			zoom: 15
		});

		infowindow = new google.maps.InfoWindow();
		var service = new google.maps.places.PlacesService(map);
		service.nearbySearch({
			location: convergence ,
			radius: 1000,
			type: ['restaurant']
		}, callback);
	}

	function callback(results, status) {
		bounds = new google.maps.LatLngBounds();
		if (status === google.maps.places.PlacesServiceStatus.OK) {
			for (var i = 0; i < results.length; i++) {
				createMarker(results[i]);
			}
			map.fitBounds(bounds);

		}
	}

	function createMarker(place) {
		var placeLoc = place.geometry.location;
		var marker = new google.maps.Marker({
			map: map,
			position: place.geometry.location
		});
		bounds.extend(marker.position);


		google.maps.event.addListener(marker, 'click', function() {
			infowindow.setContent(place.name);
			infowindow.open(map, this);
		});
	}
