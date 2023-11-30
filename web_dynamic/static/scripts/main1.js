/* Show the menu */
$(document).ready(function(){
   // animation on scroll
    const An= ScrollReveal({
        distance: '70px',
        duration: 2500,
        delay: 400,
        reset: true
    });

    An.reveal('.text', {delay: 200, origin: 'top'});
    An.reveal('.form-container form', {delay: 800, origin: 'left'});
    An.reveal('.heading', {delay: 800, origin: 'top'});
    An.reveal('.ride-container .box', {delay: 600, origin: 'bottom'});
    An.reveal('.service-container .box', {delay: 800, origin: 'bottom'});
    // changing 'booked Now' to 'Booked' and vice versa
    $(document).on('click', '.btn', function() {
		var $button = $(this);
		var carId = $button.data("id");
		var carStatus = $button.data("status")
		var newStatus = carStatus === 'unbooked' ? 'Booked' : 'unbooked';
		$.ajax({
            url: `http://127.0.0.1:5001/api/v1/update_car_status/${carId}/${newStatus}`,
            method: 'POST',
            success: function(data) {
                if (data.success) {
                    toggleBooking($button);
                } else {
                    console.error('Error updating status');
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
		//if (carStatus === 'unbooked') {
			//toggleBooking(this); // 'this' refers to the clicked element
		//}


    });

	$(document).on('click', '.btn1', function() {
		if ($(".heading2 h1").length === 0) {
			$(".heading2").append('<h1>Our Top Deals</h1>');
		}
	});

    /*function toggleBooking(element) {

        
        var $element = $(element); 
        $('.service-container.box.btn').append('<img src="assets/images/checkmark-icon.png" class="icon" alt="">');

    
        if ($element.text() === "Book Now") {
            $element.text("Booked").addClass("secondary");
        } else {
            $element.text("Book Now").removeClass("secondary");
            
        }
    }*/
	
    function toggleBooking($button) {
        //var $element = $(element); // 'this' refers to the clicked element
    
        // Check if the button has already been clicked and the booking is made
        if ($button.hasClass('booked')) {
            $button.text("Book Now");
            $button.removeClass('booked secondary');
            $button.find('.icon').remove(); // Remove the checkmark icon when unbooking
        } else {
            $button.text("Booked");
            $button.addClass('booked secondary');
            // Only append the checkmark if it doesn't exist
            if ($button.find('.icon').length === 0) {
                $button.append('<img src="../static/images/checkmark-icon.png" class="icon" alt="Checkmark">');
                An.reveal($button.find('.icon').get(0), {
                    duration: 200, // Duration of the animation
                    scale: 0.65,
                    distance: '0px',
                    easing: 'ease-in',
                    opacity: 0,
                    afterReveal: function (domelement) {
                        // domelement is the DOM element that was animated
                        // Ensure the icon stays visible after the animation, if needed
                        $(domelement).css('opacity', 1);
                    }
                });
        
                // showing the icon since it starts with 'display: none;'
                $button.find('.icon').show();

            }
        }
    }
    
	// Letting submit button to work with every chosen location and price
	var listCheckedLocation = [];
	var listCheckedPrice = [];

	$('#location').change(function() {
	
	// Reset the contents of listCheckedLocation
    listCheckedLocation = [];

    // Use jQuery to get the selected option element
    var selectedOption = $(this).find('option:selected');

    // Retrieve the data-id and data-name attributes from the selected option
    var locationId = selectedOption.data('id');
	//var locationName = selectedOption.data('name');

    // Store the retrieved values in the listCheckedLocation object
    listCheckedLocation.push(locationId);
	
	});

	
	$('#price').change(function() {

    // Reset the contents of listCheckedPrice
    listCheckedPrice = [];

    // Use jQuery to get the selected option element
    var selectedOption = $(this).find('option:selected');

    // Retrieve the data-id and data-name attributes from the selected option
    var priceId = selectedOption.data('id');
	//var priceName = selectedOption.data('name');
    // Store the retrieved values in the listCheckedPrice object
    listCheckedPrice.push(priceId);

    });
	



	$('.btn1').click(function () {
    $('.service-container').empty();
    //const dataLo = Object.keys(listCheckedLocation);
    //let dataPr = Object.keys(listCheckedPrice);
	//dataPr = dataPr.map(item => parseInt(item, 10));
    $.ajax({
      type: 'POST',
      data: JSON.stringify({ 'location': listCheckedLocation, 'price': listCheckedPrice}),
      contentType: 'application/json',
      url: 'http://127.0.0.1:5001/api/v1/car_search/',
      dataType: 'json',
      success: function (data) {
        for (const car of data) {
		  images = {"Ford Cabriolet": "https://pixabay.com/get/gbafd0d4fd36fa1c0b1d751656d22fb54655d51ca6667a46ed1f32c6a21db254f016797f7d6c8e9be4fe23dd1fec7db36aea2443517571178860490387164aef8_640.png",
                    "Renault": "https://pixabay.com/get/g55a8ae655003e3c082fdf3bc01cf74d034d6099b0870b791b6a7949f690408e2d7d38fd4c30895e1479c0453aa844a873843cdd9db6a8897277c758c6c824b8d_640.png",
					"Mercedes Benz 219": "https://pixabay.com/get/gfff0a82d86b4306217e338fce392aace75ebc880a1923a2e1f697d58a621ae1f9994bffc0e5bfa5f868427c4bc9a1be80ac9658f86b6d6913a080fded46f57ca_640.png",
					"Bmw 507": "https://pixabay.com/get/gef43966d49918deaeebf4559192c33aefde3c65b83b286e062966cadb13c59066a46e931090574c673e6a85c3370dc578cd4414cb4ff5b26d0b87c7346ec1336_640.png",
					"Auto Union 1000s": "https://pixabay.com/get/g9f753813dcb370a0677f04a09b589f8420643f28f888fb5ed2b0435c3df32a69d421f3299467a3bcce1921b18d2efef93716e21285f6938a8f748c41b0546501_640.png",
					"Mercedes Benz 220a":"https://pixabay.com/get/g0159a4df678e0c202b0f483f286120968a1ded5da549d5f3b7697a4725deaf9be595f11ef42a08dfb0e6addd94563bf6280e877ffc481443dc080d94caabf1e9_640.png",
					"Citroen Traction": "https://pixabay.com/get/g12823c3cdff21f9293910f3042c3075baf5392987851e83ee4e09d7048b7b261e050c23f4d3169eac24eb1432fb593255099217fbf6347e36726af3dab5f419b_640.png",
					"Chevrolet Corvette": "https://pixabay.com/get/g32cfcad6fa76823571f7f89e851586fce0b9aea75c10d467c9c6619c30d0b3884b54f3411b3817d666fb9c83184f3b0ebf3681b1b4e689d5b051599b14d06cf4_640.png",
					"Porsche 911": "https://pixabay.com/get/g67bc1bdd8f4b600c74f4bc8e6de278b3be95f62d9feb88557a652c41937435041c421c8dcbe591bff3721acd5603c6d34c9bd99a9c97f0a0bfded93b27e233b2_640.png"}
          $('.service-container').append(`
        <div class="box">
          <div class="box-img">
			<img src="${images[car.name]}" alt="Descriptive Text">
		  </div>
		  <h2 class="car">${car.name}</h2>
		  <h3 class="fuel">Fuel --->  ${car.fuel}</h3>
		  <h3 class="price">Price ---> <span> ${car.rent_price}$ </span>/Day</h3>
		  <a href="#services" class="btn" data-id="${car.id}" data-status="${car.status}">Book now</a>
	    </div>`);

		  $('.service-container .btn').each(function() {
            var status = $(this).data('status');
            if (status === 'Booked') {
                $(this).addClass('booked secondary');
				$(this).text("Booked");
            }
          });
        }
      }
    });
  });

});
