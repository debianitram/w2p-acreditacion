$(document).on('click', '.remove-item',
    function(event){
        Item = $(event.currentTarget).parent('li')[0];
        if (!Item){
            Item = $(event.currentTarget).parents('tr')[0];
        }

        target = Item.dataset.target;

        if (Item.dataset.db == 'true'){
            $.get("/init/curso/delete_item/",
                {'target': target},
                function(data){
                    $(Item).slideToggle();
                }
            );
        } else {
            $(Item).remove();  // Sin impacto en db.
        }
    }
);


$('#scrollable-dropdown-menu .typeahead').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 4,
    },
    {
        limit: 15,
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

            item = "<li class='list-group-item' data-target='inscripto-[id-inscripto]' data-db='false'> \
                        <a class='btn btn-xs remove-item'><span class='glyphicon glyphicon-minus-sign'></span></a> \
                        <input type='hidden' name='curso_inscripto', value='[id-inscripto]'> \
                        [value-inscripto] \
                    </li>";

            item = item.replace(new RegExp("\\[id-inscripto]", "g"), inscripto_id);
            item = item.replace("[value-inscripto]", inscripto_name);

            $('.list-group').append(item);
        }
        // Reset
        $('#typeahead-id').val('');
        $('#curso-inscripto').val('');
    }
);

$('#add-fecha').on('show.bs.collapse', function () {
    $('#add-docente').collapse('hide');
});

$('#add-docente').on('show.bs.collapse', function () {
    $('#add-fecha').collapse('hide');
});

$(document).on('click', '.actions',
        function(event) {
            Button = $(event.currentTarget);
            
            url = '/init/inscripto/actions_view/{actions}/{target}'
            url = url.replace('{actions}', Button.data('action'));
            url = url.replace('{target}', Button.parents('tr').data('target'))

            $.get(url, {}, function(data){
                result = JSON.parse(data);
                btn = result['btn'];
                content = result['content'];
                $('.modal').find('#titulo').html(Button.data('title'));
                $('.modal').find('#contenido').html(content);
                $('.modal').find('.btn-ok').html(btn);
                $('.modal').modal('show');
            });
        }
    );