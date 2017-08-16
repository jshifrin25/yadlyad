(function($, window, undefined) {
    var quantityFilter, replaceInputField, createOptions, initEvents;
    var order = {
        quantityLimits: null,
        init: function() {
           order.quantityLimits = $('.quantity').filter(quantityFilter);
           replaceInputField();
           initEvents(); 
           return order;
        }
    };
    
    initEvents = function() {
       $('input:reset').on('click',  function(e) {e.preventDefault(); $.post('reset/', {order: $('#orderId').val() })
       .done(function(data) {
                for(key in data) {
                    $('div.product-name:contains("' + key + '")+div.quantity').children().val(data[key]);
                }
           });
        });    
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
        var val = parseInt($origin.children('input').val());
        var limit = $origin.data('quantityLimit');
        for(var i = 0; i <= limit; i++) {
            var $option = $('<option></option>');
            console.log(val);
            if (val === i) {
                $option.prop('selected', true);
            }
            $option.val(i).text(i).appendTo(select);
        }
        return select;
    };
    function getCookie(name) {
        var cookieValue = null;
        if(document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            cookieStr = cookies.find(function(cookie) {
                    var cook = $.trim(cookie);
                    return cook.substring(0, name.length + 1) === (name + '=');
                }); 
             cookieValue = decodeURIComponent(cookieStr.substring(name.length + 1));   
        }
        return cookieValue;
    }
    
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));    
    }
    $(function(){
        order.init();
        var csrfToken = getCookie('csrftoken');
        $.ajaxSetup({
           beforeSend: function(xhr, settings) {
               if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
               }   
            }    
        });
    });
})(jQuery, window);
