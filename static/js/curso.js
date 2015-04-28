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

$('.remove-item-nodb').on('click',
    function(event){
        Item = $(this).parent()[0];
        Item.remove();
    }
);


$('.typeahead').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 4
    },
    {
        name: 'states',
        displayKey: 'value',
        source: function (query, process) {
            var self = this;
            self.map = {};
            return $.get("/init/persona/persona_ajax", 
                        {'query': query},
                        function(data){
                            result = JSON.parse(data);
                            $.each(result, function(id, item){
                                self.map[item.value] = item.id;
                            });
                            return process(result);
                        }
            );
        },
    }
    
).bind("typeahead:selected", function(obj, datum, name) {
    $('#typeahead-id').val(datum.id);
});

$('.new-inscripto').on('click',
    function(event){
        inscripto_id = $('#typeahead-id').val();
        inscripto_name = $('#curso-inscripto').val();

        if ((inscripto_id) && (inscripto_name)){

            UL      = $('.list-group');
            item = "<li class='list-group-item' id='inscripto-[id-inscripto]'> \
                        <a class='btn btn-xs remove-item-nodb'><span class='glyphicon glyphicon-minus-sign'></span></a> \
                        <input type='hidden' name='curso_inscripto', value='[id-inscripto]'> \
                        [value-inscripto] \
                    </li>";

            item = item.replace(new RegExp("\\[id-inscripto]", "g"), inscripto_id);
            item = item.replace("[value-inscripto]", inscripto_name);

            $('.list-group').append(item);

            // Reset
            $('#typeahead-id').val('');
            $('#curso-inscripto').val('');
        }
    }
);

$('#add-fecha').on('show.bs.collapse', function () {
    $('#add-docente').collapse('hide');
});

$('#add-docente').on('show.bs.collapse', function () {
    $('#add-fecha').collapse('hide');
})

