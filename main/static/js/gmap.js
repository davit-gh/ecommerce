function initialize() {
    var mapOptions = {
        zoom: 15,
        center: new google.maps.LatLng(49.1678136, 16.5671893),
        mapTypeId: google.maps.MapTypeId.ROAD,
        scrollwheel: false
    }
    var map = new google.maps.Map(document.getElementById('map'),
        mapOptions);

    var myLatLng = new google.maps.LatLng(49.1681989, 16.5650808);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map
    });
}

google.maps.event.addDomListener(window, 'load', initialize);
