var marker;
var Map;
var mapMarkers = new Array();

var rectangle = new google.maps.Rectangle();
var polyGon = new google.maps.Polygon();
var polyLine = new google.maps.Polyline();
var outlineMarkers = new Array();

var mapOptions = {
    center: new google.maps.LatLng(37.574361, -95.675294),
    panControl: true,
    zoom: 3,
    zoomControl: true,
    zoomControlOptions: {
        style: google.maps.ZoomControlStyle.SMALL
    }
};

$(document).ready(function(){
    $('#map_canvas').animate({
        "opacity": 1
    });
    
    Map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    
    var isClosed = false;
    
    polyLine = new google.maps.Polyline({
        map: Map,
        path: [],
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    
    polyGon = new google.maps.Polygon({
        map: Map,
        path: [],
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#FF0000",
        fillOpacity: 0.35,
        draggable: true
    });
    
    //ability to drag the polygon around
    google.maps.event.addListener(polyGon, "drag", function (dragEvent) {
        var polyGonPoints = this.getPath().getArray();
        $.each(polyGonPoints, function (index, val) {
            var polyGonPoint = val;
            outlineMarkers[index].setPosition(polyGonPoint);
        });
        //Hypothetical function that enters each point into textboxes (for form submission, for example) - I didn't write this function, but this is when you'd call it...
        //updateTxtPolygon();
    });
    /* //remove polygon on right-click?
    google.maps.event.addListener(polyGon, "rightclick", function (dragEvent) {
        removePolygon();
        
        //Hypothetical function - see above
        //updateTxtPolygon();
    });
    */

    google.maps.event.addListener(Map, "rightclick", function (event) {
        //event.preventDefault();
       
        var markerIndex = polyLine.getPath().length;
        polyLine.setMap(Map);
        var isFirstMarker = markerIndex === 0;
        var marker = new google.maps.Marker({
            map: Map,
            position: event.latLng,
            draggable: true
        });
        
        
        //google.maps.event.addListener(marker, 'dragend', function () {
        //          Hypothetical function - see above
        //          updateTxtPolygon();
        //      });
        
        if (isFirstMarker) {
            google.maps.event.addListener(marker, 'click', function () {
                var path = polyLine.getPath();
                polyGon.setPath(path);
                polyGon.setMap(Map);
            });
            // we were setting different colored icons so you could tell which was the last point set
            //    marker.setIcon(blueIcon);
        } else {
            //    marker.setIcon(yellowIcon);
        }
        
        
        google.maps.event.addListener(polyLine, 'click', function(clickEvent){
            //did you want to do something here??
        });
        
        polyLine.getPath().push(event.latLng);
        
        //different colored markers so user can tell which was the first marker the placed
        //if(markerIndex > 1)
        //    outlineMarkers[markerIndex-1].setIcon(blueIcon);
        
        outlineMarkers.push(marker);
                
        google.maps.event.addListener(marker, 'drag', function (dragEvent) {
            polyLine.getPath().setAt(markerIndex, dragEvent.latLng);
            updateDistance(outlineMarkers);
        });
        
        updateDistance(outlineMarkers);
    });   
    
});

function updateDistance(outlineMarkers){
    var totalDistance = 0.0;
        var last = undefined;
        $.each(outlineMarkers, function(index, val){
            if(last){
                console.log(google.maps.geometry.spherical.computeDistanceBetween(last.position, val.position));
                totalDistance += google.maps.geometry.spherical.computeDistanceBetween(last.position, val.position);
            }
            last = val;
        });
        
        $("#txtDistance").val(totalDistance);
}