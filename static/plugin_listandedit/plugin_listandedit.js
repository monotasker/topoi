$(document).ready(function(){

/* set listpane height to optimal */
/* if pane heights are wrong, change the value of the heightadjust variable to tweak it */
var heightadjust = 0;
var lpos = $('#listpane').offset();
var vpos = $('#viewpane').offset();
var listtop = lpos.top;
var viewtop = vpos.top;
var winheight = $(window).height();
/* I'm using the html5 footer element here, to use standard id just change 'footer' to '#footer' */
var footheight = $('#footer').height();
//var footmargin = $('#footer').css('margin-top');
//var pagepadding = $('#page').css('padding-bottom');
var listheight = winheight - listtop - footheight - heightadjust;
var viewheight = winheight - viewtop - footheight - heightadjust;
$('#listpane').css('height', listheight);
$('#viewpane').css('height', viewheight);

/* make sure pane heights resize properly when window resizes */
$(window).bind('resize', function(){
    $('#listpane').css('height', listheight);
    $('#viewpane').css('height', viewheight);
});

})
