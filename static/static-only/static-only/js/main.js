document.addEventListener('DOMContentLoaded', function() {
    var navbarItems = document.querySelectorAll('.navbar li');
  
    navbarItems.forEach(function(item) {
      item.addEventListener('click', function() {
        navbarItems.forEach(function(item) {
          item.classList.remove('active');
        });
  
        this.classList.add('active');
      });
    });
});
