$(document).ready(function(){

    // Equal Height
    $("#HmSecFeatures .feature-content").matchHeight();
    $("#AbSecActions .feature-content").matchHeight();

    // Smooth Scrolling
    $('[href*="#"].smooth').click(function() {

        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') 
            || location.hostname == this.hostname) {

            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
              if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });

});