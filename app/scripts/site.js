/**
 * @name Site
 * @description Define global variables and functions
 * @version 1.0
 */
var Site = (function($, window, undefined) {
  var html = $('html');

  function isMobile() {
    return window.Modernizr.mq('(max-width: 767px)');
  }

  function init() {
    if (html.is('.ie8') || html.is('.ie9')) {
      $('[placeholder]').placeholder();
    }
  }

  return {
    init: init,
    isMobile: isMobile
  };

})(jQuery, window);

jQuery(function() {
  Site.init();
});
