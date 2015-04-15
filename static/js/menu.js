/*   MENU  DROPDOWN AOM */
$(".dropdown").hover(
    function(){
        $('.dropdown-menu', this).stop(true, true).slideDown("medium");
        $(this).toggleClass('open');        
    },
    function(){
        $('.dropdown-menu', this).stop(true, true).slideUp("medium");
        $(this).toggleClass('open');       
    }
);