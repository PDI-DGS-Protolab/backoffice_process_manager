
$(function() {

    /* Global Vars */

    var details  = $('.process');
    var articles = $('.subprocess');
    var moreInfo = $('.more-info');


    /* Handlers */

    var detailHandler = function() {
    	var index = $(this).index();
    	articles.animate({
            "margin-left" : "-300px",
            "opacity"     : "0"
        }, 500);

        articles.eq(index).animate({
            "margin-left" : "0px",
            "opacity"     : "1"
        }, 500);
    }

    var externalResultsHandler = function() {
        var chevron = $(this).children();
        chevron.toggleClass('icon-chevron-down icon-chevron-up');

        var index = $(this).parent().index();

        var visibleArticle = articles.filter(function(i) {
            return !articles.eq(i).hasClass('hidden');
        })

        var rows = visibleArticle.find('.tasks').children();
        rows.eq(index + 1).fadeToggle();
    }


    /* Event Assignments */

    details.on('click', detailHandler);
    moreInfo.on('click', externalResultsHandler);

});
