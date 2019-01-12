(function worker() {
  $.ajax({
    url: 'ajax/all-bookables',
    success: function(data) {
      $('#all-bookables').html(data);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(worker, 5000);
    }
  });
})();

book = function(btn) {
  $.ajax({
    url: 'ajax/book',
    data: {
      'time': btn.value,
    },
    success: function (data) {
      if (data['error'] == true)
      //console.log(data);
        alert(data['message']);
    },
    complete: function() {
      location.reload()
    }
  });
  btn.innerText = 'pending';
  children = document.getElementById('all-bookables').children;
  for (var i =0; i < children.length; i++)
    children[i].disabled = true;
}
