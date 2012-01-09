$('#{{=linktable}}_add_trigger').live('click', function(event){
        var adder_dialog = $('<div id="{{=linktable}}_adder_form" class="ajaxselect_adder_form">{{=P("hi there")}}</div>');
        adder_dialog.dialog({
            height:200,
            width:500
        });
    });
