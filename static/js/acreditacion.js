/*   MENU  DROPDOWN AOM */

$(document).ready(function(){
    $(".dropdown").hover(            
        function() {
            $('.dropdown-menu', this).stop( true, true ).slideDown("medium");
            $(this).toggleClass('open');        
        },
        function() {
            $('.dropdown-menu', this).stop( true, true ).slideUp("medium");
            $(this).toggleClass('open');       
        }
    );

    $('#btn-agregar-fecha').click(function(){
      $('.div-agregar-fecha').toggle();
    });

    $('#btn-agregar-docente').click(function(){
      $('.div-agregar-docente').toggle();
    });

});