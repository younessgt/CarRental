$(document).ready(function(){
	$(document).on('click', '.delete_btn', function () {

		const $button = $(this);
		const carId = $button.data('id');
		const carStatus = $button.data('status');
		const newStatus = 'unbooked';
		const userId = currentUserId;
		if (carStatus === 'Booked') {
			$.ajax({
				url: `http://127.0.0.1:5001/api/v1/update_car_status/${carId}/${newStatus}/${userId}`,
				method: 'POST',
				success: function (data) {
					if (data.success) {
						//toggleBooking($button);
					} else {
						console.error('Error updating status');
					}
				},
			error: function (error) {
				console.error('Error:', error);
			}
			});
		}
		$(this).closest('section').remove();
		// .closest('section') finds the nearest ancestor 'section' element
        	// .remove() removes the element from the DOM
    });
});
