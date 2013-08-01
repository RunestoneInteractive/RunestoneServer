/*
 * jQuery Hotkeys Plugin
 * Copyright 2010, John Resig
 * Dual licensed under the MIT or GPL Version 2 licenses.
 *
 * Based upon the plugin by Tzury Bar Yochay:
 * http://github.com/tzuryby/hotkeys
 *
 * Original idea by:
 * Binny V A, http://www.openjs.com/scripts/events/keyboard_shortcuts/
*/
(function(e){function g(a){"string"===typeof a.data&&(a.data={keys:a.data});if(a.data&&a.data.keys&&"string"===typeof a.data.keys){var g=a.handler,h=a.data.keys.toLowerCase().split(" "),k="text password number email url range date month week time datetime datetime-local search color tel".split(" ");a.handler=function(c){if(this===c.target||!(/textarea|select/i.test(c.target.nodeName)||-1<e.inArray(c.target.type,k))){var d=e.hotkeys.specialKeys[c.keyCode],a="keypress"===c.type&&String.fromCharCode(c.which).toLowerCase(),
b="",f={};c.altKey&&"alt"!==d&&(b+="alt+");c.ctrlKey&&"ctrl"!==d&&(b+="ctrl+");c.metaKey&&(!c.ctrlKey&&"meta"!==d)&&(b+="meta+");c.shiftKey&&"shift"!==d&&(b+="shift+");d&&(f[b+d]=!0);a&&(f[b+a]=!0,f[b+e.hotkeys.shiftNums[a]]=!0,"shift+"===b&&(f[e.hotkeys.shiftNums[a]]=!0));d=0;for(a=h.length;d<a;d++)if(f[h[d]])return g.apply(this,arguments)}}}}e.hotkeys={version:"0.8",specialKeys:{8:"backspace",9:"tab",10:"return",13:"return",16:"shift",17:"ctrl",18:"alt",19:"pause",20:"capslock",27:"esc",32:"space",
33:"pageup",34:"pagedown",35:"end",36:"home",37:"left",38:"up",39:"right",40:"down",45:"insert",46:"del",96:"0",97:"1",98:"2",99:"3",100:"4",101:"5",102:"6",103:"7",104:"8",105:"9",106:"*",107:"+",109:"-",110:".",111:"/",112:"f1",113:"f2",114:"f3",115:"f4",116:"f5",117:"f6",118:"f7",119:"f8",120:"f9",121:"f10",122:"f11",123:"f12",144:"numlock",145:"scroll",186:";",191:"/",220:"\\",222:"'",224:"meta"},shiftNums:{"`":"~",1:"!",2:"@",3:"#",4:"$",5:"%",6:"^",7:"&",8:"*",9:"(",0:")","-":"_","=":"+",";":": ",
"'":'"',",":"<",".":">","/":"?","\\":"|"}};e.each(["keydown","keyup","keypress"],function(){e.event.special[this]={add:g}})})(this.jQuery);
