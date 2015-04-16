/*   MENU  DROPDOWN AOM */
$(".dropdown").hover(
    function(){
        $('.dropdown-menu', this).stop(true, false).slideDown("medium");
        $(this).toggleClass('open');        
    },
    function(){
        $('.dropdown-menu', this).stop(true, false).slideUp("medium");
        $(this).toggleClass('open');       
    }
);

