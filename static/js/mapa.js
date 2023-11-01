google.maps.event.addDomListener(window,"load",function(){
    const ubicacion= new Localizacion(()=>{
        const myLatLng= {lat: ubicacion.latitude, lng: ubicacion.longitude};

        var texto='<h1> Nombre del lugar </h1>' + '<p> Descripción de lugar </p>'+ '<a href="https://www.google.com"> Página web</a>';

        const options = {
            center:myLatLng,
            zoom:14
        }

        var map=document.getElementById('map');

        const mapa= new google.maps.Map(map,options);

        const marcador= new google.maps.Marker({
            position: myLatLng,
            map: mapa,
            title:"Mi primer marcador"
        });

        var informacion= new google.maps.InfoWindow({
            content: texto
        });

        marcador.addListener('click', function(){
            informacion.open(mapa,marcador);
        });

        var autocomplete=document.getElementById('autocomplete');
        const search=google.maps.places.Autocomplete(autocomplete);
        search.bindTo("bounds",mapa);
    });

});