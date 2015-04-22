$('#curso-inscriptos').dataTable();

$('.remove-item').on('click',
    function(event){
        Item = $(this).parent()[0];
        target = Item.dataset.target;

        $.get("/init/curso/delete_item/",
            {'target': target},
            function(data){
                $('*[data-target='+data+']').slideToggle();
            }
        );
    }
);