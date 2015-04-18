$(document).ready(function(){

    $('.remove-item').on('click',
        function(event){
            Item = $(this).parent()[0];
            target = Item.dataset.target;

            $.get("/acreditacion/curso/delete_item/",
                {'target': target},
                function(data){
                    console.log(data);
                }
            );
        }
    );

    $('#add-docente .typeahead').typeahead(
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
                return $.get("/acreditacion/persona/persona_ajax", 
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
        $('#inscripto-docente-id').val(datum.id);
    });
});