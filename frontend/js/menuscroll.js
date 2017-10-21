$(window).on("scroll", function() {
  if($(window).scrollTop() > 20) {
    console.log('add class menu-bar-scrolled');
    $(".menu-bar").addClass("menu-bar-scrolled");
  }
  else {
    console.log('remove class menu-bar-scrolled');
    $(".menu-bar").removeClass("menu-bar-scrolled");
  }
});
