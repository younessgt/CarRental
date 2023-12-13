/* Show the menu */
$(document).ready(function () {
  // user login
  $('#login-btn').on('click', function () {
    $('#login').addClass('show-login');
  });

  $('#login-close').on('click', function () {
    $('#login').removeClass('show-login');
  });

  // Check URL for 'form' parameter
  const urlParams = new URLSearchParams(window.location.search);
  const formToShow = urlParams.get('form');

  if (formToShow === 'signup' || formToShow === 'signin') {
    $('#login').addClass('show-login');
  }

  // Show the appropriate form based on the parameter
  if (formToShow === 'signup') {
    $('#login-signin').hide();
    $('#login-signup').show();
  } else if (formToShow === 'signin') {
    $('#login-signup').hide();
    $('#login-signin').show();
  }

  $('#signup-btn').click(function(e) {
    e.preventDefault();
    $('#login-signin').hide();
    $('#login-signup').show();
  });

  $('#signin-btn').click(function(e) {
    e.preventDefault();
    $('#login-signup').hide();
    $('#login-signin').show();
  });
  // Animate Background
  const backgrounds = [
    'url("../static/images/Backround2.webp")',
    'url("../static/images/Backround1.webp")'
  ];

  let currentBack = 0;

  // insuring that all background images are loaded by the browser
  function preloadImages () {
    for (let i = 0; i < backgrounds.length; i++) {
      $('<img/>')[0].src = backgrounds[i].slice(5, -2); // Remove 'url(' and ')' from the string
    }
  }

  // function to change to background image
  function changeBackground () {
    $('.home').css('background-image', backgrounds[currentBack]);
    currentBack = (currentBack + 1) % backgrounds.length;
  }

  preloadImages();

  setTimeout(function () {
    changeBackground(); // change immediately
    // start the interval and change images every 3s
    setInterval(changeBackground, 3000);
  }, 3000);

  // Making every click on each <a> tag which is a button in our case
  // go to the entire section
  $('a[href^="#"]').click(function (e) {
    e.preventDefault();
    const targetID = $(this).attr('href');
    const target = $(targetID);

    if (target.length) {
      const headerHeight = $('header').outerHeight(); // Calculate the height of the header
      const position = target.offset().top - headerHeight;
      $('html, body').animate({
        scrollTop: position // Offset the scroll position
      }, 380); // Duration of the scrolling animation
    }
  });

  // animation on scroll
  const An = ScrollReveal({
    distance: '70px',
    duration: 2500,
    delay: 400,
    reset: true,
    beforeReveal: function (domEl) {
      $(domEl).css('visibility', 'visible'); // Make elements visible before animation
    }
  });

  An.reveal('.text', { delay: 200, origin: 'top' });
  An.reveal('.form-container form', { delay: 800, origin: 'left' });
  An.reveal('.heading', { delay: 800, origin: 'top' });
  An.reveal('.ride-container .box', { delay: 600, origin: 'bottom' });
  An.reveal('.service-container .box', { delay: 800, origin: 'bottom' });
  // changing 'booked Now' to 'Booked' and vice versa
  $(document).on('click', '.btn', function () {
    const $button = $(this);
    const carId = $button.data('id');
    const carStatus = $button.data('status');
    const newStatus = 'Booked';
	const userId = currentUserId;
	if (carStatus === 'unbooked') {
      $.ajax({
        url: `http://127.0.0.1:5001/api/v1/update_car_status/${carId}/${newStatus}/${userId}`,
        method: 'POST',
        success: function (data) {
          if (data.success) {
            toggleBooking($button);
          } else {
            console.error('Error updating status');
          }
        },
        error: function (error) {
          console.error('Error:', error);
        }
      });
	}
  });

  $(document).on('click', '.btn1', function () {
    if ($('.heading2 h1').length === 0) {
      $('.heading2').append('<h1>Our Top Deals</h1>');
    }
  });

    function toggleBooking ($button) {

    // Check if the button has already been clicked and the booking is made
    if ($button.hasClass('booked')) {
      $button.find('.icon').remove(); // Remove the checkmark icon when unbooking
    } else {
      $button.text('Booked');
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
  let listCheckedLocation = [];
  let listCheckedPrice = [];

  $('#location').change(function () {
    // Reset the contents of listCheckedLocation
    listCheckedLocation = [];

    // Use jQuery to get the selected option element
    const selectedOption = $(this).find('option:selected');

    // Retrieve the data-id and data-name attributes from the selected option
    const locationId = selectedOption.data('id');
    // var locationName = selectedOption.data('name');

    // Store the retrieved values in the listCheckedLocation object
    listCheckedLocation.push(locationId);
  });

  $('#price').change(function () {
    listCheckedPrice = [];

    const selectedOption = $(this).find('option:selected');

    const priceId = selectedOption.data('id');
    listCheckedPrice.push(priceId);
  });

  $('.btn1').click(function () {
    $('.service-container').empty();
    $.ajax({
      type: 'POST',
      data: JSON.stringify({ location: listCheckedLocation, price: listCheckedPrice }),
      contentType: 'application/json',
      url: 'http://127.0.0.1:5001/api/v1/car_search/',
      dataType: 'json',
      success: function (data) {
        for (const car of data) {
          const imageName = car.name.replace(/\s+/g, '-');
		  var buttonHtml = isUserAuthenticated
                ? `<a href="javascript:void(0);" class="btn" data-id="${car.id}" data-status="${car.status}">Book now</a>`
                : `<a href="/signin" class="btn3" data-id="${car.id}" data-status="${car.status}">Book now</a>`;
          $('.service-container').append(`
        <div class="box">
          <div class="box-img">
            <img src="../static/images/${imageName}.png" alt="Descriptive Text">
          </div>
          <h2 class="car">${car.name}</h2>
          <h3 class="fuel">Fuel --->  ${car.fuel}</h3>
          <h3 class="price">Price ---> <span> ${car.rent_price}$ </span>/Day</h3>
		  ${buttonHtml}
		  </div>`);
          // after refreshing the page and clicking submit again
          // we check each btn to see it status which is gotten from the database
          // if the status is Booked the button color should be green
          $('.service-container .btn').each(function () {
            const status = $(this).data('status');
            if (status === 'Booked') {
              $(this).addClass('booked secondary');
              $(this).text('Booked');
            }
          });
        }
      }
    });
  });
});
