$('.add_trigger').live('click', function(event){
    var the_id = $(this).attr('id');
    var parts = the_id.split('_');
    var linktable = parts[0];

    $('#' + linktable + '_adder_form').dialog({
        height:200,
        width:500,
        title:'Add new '
    });
});

$('.restrictor').live('change', function(event){
    var new_val = $(this).find('option:selected').val();
    var parts = $(this).attr('id').split('_');
    var table = parts[0];

    var classlist = $(this).attr('class').split(/\s+/);
    $.each(classlist, function(index,item){
       if(item.substring(0,4) == 'for_'){
           field = item.substring(4);

           var span_id = table + '_' + field + '_loader'
           var r_url = $('#' + span_id).next().attr('href')
           r_url += '/' + new_val;

           web2py_component(r_url, span_id);
       }
    });
});