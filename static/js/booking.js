
(function worker() {
  $.ajax({
    url: 'ajax/booked',
    success: function(data) {
      if (data['booked'] == false)
        location.reload();
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(worker, 5000);
    }
  });
})();

release = function(btn) {
  $.ajax({
    url: 'ajax/release-booking',
    complete: function() {
      location.reload();
    },
  });
  btn.innerText = 'Releasing';
  btn.disabled = true; // TODO fix this
}
