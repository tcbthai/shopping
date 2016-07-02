/**
 *  @name toggle-target
 *  @description description
 *  @version 1.0
 *  @options
 *    option
 *  @events
 *    event
 *  @methods
 *    init
 *    publicMethod
 *    destroy
 */
;(function($, window, undefined) {
  var pluginName = 'toggle-target',
    container = $('.container');

  function Plugin(element, options) {
    this.element = $(element);
    this.options = $.extend({}, $.fn[pluginName].defaults, this.element.data(), options);
    this.init();
  }

  Plugin.prototype = {
    init: function() {
      var that = this;

      that.vars = {
        clickElm: that.element.find(that.options.clickElm),
        wrapper: that.element.find(that.options.target),
        isMobile: Site.isMobile()
      };

      that.vars.clickElm
        .off('click.' + pluginName)
        .on('click.' + pluginName, function(e) {
          e.preventDefault();
          var clickedElm = $(this),
            item = clickedElm.closest(that.options.target);
          item.toggleClass(that.options.openClass);
          that.vars.clickElm.not(clickedElm).closest(that.options.target).removeClass(that.options.openClass);
        });
      if (that.options.activeHover) {
        that.vars.wrapper
          .on('mouseenter.' + pluginName, function() {
            var item = $(this);

            item.addClass(that.options.openClass);
            that.vars.wrapper.not(item).removeClass(that.options.openClass);
          })
          .on('mouseleave.' + pluginName, function() {
            var item = $(this);

            item.removeClass(that.options.openClass);
          });
      }
      container.on('click.' + pluginName, function(e) {
        var elm = $(e.target);
        if(!elm.closest(that.element).length) {
          that.vars.wrapper.removeClass(that.options.openClass);
        }
      });
    },
    destroy: function() {
      // deinitialize
      $.removeData(this.element[0], pluginName);
    }
  };

  $.fn[pluginName] = function(options, params) {
    return this.each(function() {
      var instance = $.data(this, pluginName);
      if (!instance) {
        $.data(this, pluginName, new Plugin(this, options));
      } else if (instance[options]) {
        instance[options](params);
      } else {
        window.console && console.log(options ? options + ' method is not exists in ' + pluginName : pluginName + ' plugin has been initialized');
      }
    });
  };

  $.fn[pluginName].defaults = {
    target: '.dropdown',
    clickElm: '.dropdown-toggle',
    openClass: 'open',
    activeHover: false
  };

  $(function() {
    $('[data-' + pluginName + ']')[pluginName]();
  });

}(jQuery, window));
