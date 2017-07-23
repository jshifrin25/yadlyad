(function($, window, undefined) {
    var quantityFilter, replaceInputField, createOptions;
    var order = {
        quantityLimits: null,
        init: function() {
           order.quantityLimits = $('.quantity').filter(quantityFilter);
           replaceInputField();
           return order;
        }
    };
    quantityFilter = function(index, elem) {
      return $(elem).data('quantityLimit') > 0;
    };
    replaceInputField = function() {
      order.quantityLimits.each(function(index, elem){
         var select = createOptions(elem);
         $(elem).html(select);
      });
    };
    createOptions = function(elem) {
        var $origin;
        var select = $('<select></select>');
        $origin = $(elem);
        select.attr('name', $origin.children('input').attr('name'));
        var limit = $origin.data('quantityLimit');
        for(var i = 0; i <= limit; i++) {
            $('<option></option>').val(i).text(i).appendTo(select);
        }
        return select;
    };

    $(function(){
        order.init();
    });
})(jQuery, window);
