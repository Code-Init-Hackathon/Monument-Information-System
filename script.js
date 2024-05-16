
      async function initMap() {
        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
        const map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 47.830333, lng: 34.250423},
          zoom: 2,
          mapId: 'cfc4889586555ed7'
        });
        const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
        const iconImage =document.createElement("img");
        iconImage.src=image
        var contentString =
          '<div id="content">' +
          '<div id="siteNotice">' +
          "</div>" +
          '<h1 id="firstHeading" class="firstHeading">Uluru</h1>' +
          '<div id="bodyContent">' +
          '<img src="https://lh3.googleusercontent.com/p/AF1QipPTxHG0_dJooayYKzCB004tccRM5MhxYp6KWa53=s680-w680-h510" alt="Uluru" style="display: block;margin: 0 auto;max-width:100px;max-height:100px;width:auto;height:auto;">' +
          "<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large " +
          "sandstone rock formation in the southern part of the " +
          "Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi)</p> " +
          "</div>" +
          "</div>";

        const infowindow = new google.maps.InfoWindow({
          content: contentString,
          ariaLabel:"Uluru"
        });
        const marker = new google.maps.marker.AdvancedMarkerElement({
            map,
            //animation: google.maps.Animation.DROP,
            content: iconImage,
            title:"Hello World",
            position: {lat: 47.830333, lng: 34.250423},
          });
        
        
        marker.addListener("click", () => {
              infowindow.open({
              anchor:marker,
              map,
            });
            // Handle the click event.
            // ...
          });
      }
     
      window.initMap=initMap;