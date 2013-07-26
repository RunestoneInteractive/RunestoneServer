// revert the version of underscore and jquery to whatever it was
// before parson's code included header files

var $pjQ = jQuery.noConflict(true);
var _p = _.noConflict();
