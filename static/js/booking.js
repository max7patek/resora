release = function(btn) {
  $.ajax({
    url: 'ajax/release-booking',
    complete: function() {
      location.reload()
    },
  });
  btn.innerText = 'Releasing';
  btn.disabled = true; // TODO fix this
}
