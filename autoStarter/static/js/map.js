ymaps.ready(init);
var myMap, 
    Placemark;

function init(){ 
    myMap = new ymaps.Map("MapContacts", {
        center: [44.624398, 40.060769],
        zoom: 17
    });

    myMap.behaviors.disable('scrollZoom');

    Placemark = new ymaps.Placemark([44.624398, 40.060769], {}, {
        iconLayout: 'default#image',
        iconImageHref: '/static/images/placemark.png',
        iconImageSize: [90, 73],
        iconImageOffset: [-45, -73]
    });

    myMap.geoObjects
        .add(Placemark);
}