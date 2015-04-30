/**
 * jQuery sound plugin (no flash)
 * 
 * port of script.aculo.us' sound.js (http://script.aculo.us), based on code by Jules Gravinese (http://www.webveteran.com/) 
 * 
 * Copyright (c) 2007 Jörn Zaefferer (http://bassistance.de) 
 * 
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *   
 * $Id: jquery.sound.js 5854 2008-10-04 10:22:25Z joern.zaefferer $
 */

/**
 * API Documentation
 * 
 * // play a sound from the url
 * $.sound.play(url)
 * 
 * // play a sound from the url, on a track, stopping any sound already running on that track
 * $.sound.play(url, {
 *   track: "track1"
 * });
 * 
 * // increase the timeout to four seconds before removing the sound object from the dom for longer sounds
 * $.sound.play(url, {
 *   timeout: 4000
 * });
 * 
 * // stop a sound by removing the element returned by play
 * var sound = $.sound.play(url);
 * sound.remove();
 * 
 * // disable playing sounds
 * $.sound.enabled = false;
 * 
 * // enable playing sounds
 * $.sound.enabled = true
 */

(function($) {
	
$.sound = {
	tracks: {},
	enabled: true,
	template: function(src) {
		// todo: move bgsound element and browser sniffing in here
		// todo: test wmv on windows: Builder.node('embed', {type:'application/x-mplayer2', pluginspage:'http://microsoft.com/windows/mediaplayer/en/download/',        id:'mediaPlayer', name:'mediaPlayer', displaysize:'4', autosize:'-1', bgcolor:'darkblue', showcontrols:'false', showtracker:'-1', showdisplay:'0', showstatusbar:'-1', videoborder3d:'-1', width:'0', height:'0', src:audioFile, autostart:'true', designtimesp:'5311', loop:'false'});
		// is_win = (agt.indexOf("windows") != -1);
		return '<embed style="height:0" loop="false" src="' + src + '" autostart="true" hidden="true"/>';
	},
	play: function(url, options){
		if (!this.enabled)
			return;
		options = $.extend({
			url: url,
			timeout: 2000
		}, options);
		
		if (options.track) {
			if (this.tracks[options.track]) {
				var current = this.tracks[options.track];
				// TODO check when Stop is avaiable, certainly not on a jQuery object
				current[0].Stop && current[0].Stop();
				current.remove();  
			}
		}
		
		var element = $.browser.msie
		  	? $('<bgsound/>').attr({
		        src: options.url,
				loop: 1,
				autostart: true
		      })
		  	: $(this.template(options.url));
			
		element.appendTo("body");
		
		if (options.track) {
			this.tracks[options.track] = element;
		}
		
		setTimeout(function() {
			element.remove();
		}, options.timeout)
		
		return element;
	}
};

})(jQuery);