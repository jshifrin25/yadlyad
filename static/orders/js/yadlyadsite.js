(function($) {
  $.fn.tableHighlighter = function(options) {
    return this.each(function(index, el) {
      var $elem, opts;
      $elem = $(el);
      opts = $.extend($.fn.tableHighlighter.defaults, options);
      if (index % 2 === 0) {
        $elem.addClass(opts.oddClass);
      } else {
        $elem.addClass(opts.evenClass);
      }
      return this;
    });
  };
  $.fn.tableHighlighter.defaults = {
    evenClass: "",
    oddClass: 'highlighted-row'
  };
  return this;
})(jQuery);
;var OrderTable;

OrderTable = function(rowClass) {
  var _this = this;
  this.rowClass = rowClass;
  return $(function() {
    return $("." + _this.rowClass).tableHighlighter();
  });
};
;OrderTable("product-item-row");
