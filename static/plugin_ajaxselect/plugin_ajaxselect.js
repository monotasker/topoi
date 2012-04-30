
$('.add_trigger').live('click', function(event){
//open modal dialog (using jquery-ui dialog) for adder form
    var the_id = $(this).attr('id');
    var parts = the_id.split('_');
    var linktable = parts[0];

    $('#' + linktable + '_adder_form').html('');
    $('#' + linktable + '_adder_form').dialog({
        height:600,
        width:600,
        title:'Add new '
    });
});

$('.edit_trigger').live('click', function(event){
//open modal dialog (using jquery-ui dialog) for edit form
    var the_id = $(this).attr('id');
    var parts = the_id.split('_');
    var linktable = parts[0];

    $('#' + linktable + '_adder_form').html('');
    $('#' + linktable + '_editlist_form').dialog({
        height:600,
        width:600,
        title:'Edit '
    });
});