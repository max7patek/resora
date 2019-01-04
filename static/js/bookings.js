(function worker() {
  $.ajax({
    url: 'ajax/bookings',
    success: function(data) {
      $('#bookings').html(data);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(worker, 60000); // every minute
    }
  });
})();
