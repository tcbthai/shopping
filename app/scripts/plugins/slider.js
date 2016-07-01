/**
 *  @name slide
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
  var pluginName = 'slider';

  function Plugin(element, options) {
    this.element = $(element);
    this.options = $.extend({}, $.fn[pluginName].defaults, this.element.data(), options);
    this.init();
  }

  Plugin.prototype = {
    init: function() {
      switch (this.options.type) {
        default:
          this.initDefault();
      }
    },
    initDefault: function() {
      var that = this;

      this.element.slick({
        accessibility: false,
        autoplay: true,
        autoplaySpeed: that.options.autoplayspeed,
        infinite: false,
        pauseOnHover: false,
        slidesToShow: that.options.slidesToShow,
        slidesToScroll: that.options.slidesToScroll,
        responsive: [
        {
          breakpoint: 991,
          settings: {
            slidesToShow: that.options.slidesToShowOnMobile,
            slidesToScroll: that.options.slidesToScrollOnMobile,
          }
        }
        ]
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
    autoplayspeed: 5000,
    slickArrow: '.slick-arrow',
    slickcustomindicator: '.slider-nav-2',
    slidesToShow: 1,
    slidesToScroll: 1
  };

  $(function() {
    $('[data-' + pluginName + ']')[pluginName]();
  });

}(jQuery, window));
