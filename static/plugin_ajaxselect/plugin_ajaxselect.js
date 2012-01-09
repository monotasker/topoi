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