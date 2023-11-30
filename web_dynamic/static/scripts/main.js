/* Show the menu */
$(document).ready(function(){
   
	// Animate Background
	var backgrounds = [
		'url("../static/images/Backround2.webp")',
		'url("../static/images/Backround1.webp")'
	];

	var currentBack = 0;
	// setting the first image background immediatly
	$('.home').css('background-image', backgrounds[currentBack]);

	// function to change to background image
	function changeBackground() {

		currentBack = (currentBack + 1) % backgrounds.length;
		$('.home').css('background-image', backgrounds[currentBack]);

	}
	
	// start the interval and change images every 3s
	setInterval(changeBackground, 3000);





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
		  //images = {"Ford Cabriolet": "../static/images/Ford-Cabriolet.png",
            //        "Renault": "../static/images/Renault.png",
			//		"Mercedes Benz 219": "../static/images/Mercedes-Benz-219.png",
			//		"Bmw 507": "../static/images/Bmw-507.png",
			//		"Auto Union 1000s": "../static/images/Auto-Union-1000s.png",
			//		"Mercedes Benz 220a":"../static/images/Mercedes-Benz-219.png",
			//		"Citroen Traction": "../static/images/Mercedes-Benz-219.png",
			//		"Chevrolet Corvette": "../static/images/Bmw-507.png",
			//		"Porsche 911": "../static/images/Ford-Cabriolet.png"}
		  var imageName = car.name.replace(/\s+/g, '-')
          $('.service-container').append(`
        <div class="box">
          <div class="box-img">
			<img src="../static/images/${imageName}.png" alt="Descriptive Text">
		  </div>
		  <h2 class="car">${car.name}</h2>
		  <h3 class="fuel">Fuel --->  ${car.fuel}</h3>
		  <h3 class="price">Price ---> <span> ${car.rent_price}$ </span>/Day</h3>
		  <a href="javascript:void(0);" class="btn" data-id="${car.id}" data-status="${car.status}">Book now</a>
	    </div>`);
		  // after refreshing the page and clicking submit again 
			// we check each btn to see it status which is gotten from the database
			// if the status is Booked the button color should be green 
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
