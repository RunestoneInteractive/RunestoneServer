/**
 * Created by isaacdontjelindell on 8/2/13.
 */

/* Sets up the interactive navhelp */

var is_setup;

function setup() {
    guiders.createGuider({
        attachTo: ".navbar-brand",
        highlight: ".navbar-brand",
        overlay: true,
        title: "Table of Contents",
        description: "Click here to see the Table of Contents for this textbook.",
        id: "first",
        next: "second",
    }).show();

    guiders.createGuider({
        attachTo: ".brand-logo",
        highlight: ".brand-logo",
        overlay: true,
        title: "Homepage",
        description: "Click here to go back to the homepage, where you can see the other textbooks that are available.",
        id: "second",
        next: "third"
    });

    el = $('.nav.navbar-nav li.dropdown');
    el = $(el[4]).addClass('pagenav');
    guiders.createGuider({
        attachTo: ".pagenav",
        highlight: ".pagenav",
        overlay: true,
        title: "Page Navigation",
        description: "Click here to jump to a section within the current chapter.",
        id: "third",
        next: "fourth"
    });

    el = $('.nav.navbar-nav li.dropdown');
    el = $(el[1]).addClass('searchmenu');
    guiders.createGuider({
        attachTo: ".searchmenu",
        highlight: ".searchmenu",
        overlay: true,
        title: "Search Menu",
        description: "This menu allows you to search this textbook, as well as open a scratchpad. You can also press the '\\' (backslash) key at any time to open the scratchpad.",
        id: "fourth",
        next: "fifth"
    });

    el = $('.nav.navbar-nav li.dropdown');
    el = $(el[2]).addClass('usermenu');
    guiders.createGuider({
        attachTo: ".usermenu",
        highlight: ".usermenu",
        overlay: true,
        title: "Account Menu",
        description: "Log in or register here so that you can save and load code you write and save your position in the textbook. Don't worry, it's easy!",
        id: "fifth",
        next: "sixth"
    });

    guiders.createGuider({
        attachTo: "#codeexample1",
        highlight: "#codeexample1",
        overlay: true,
        title: "ActiveCode Blocks",
        description: "ActiveCode blocks allow you to write and execute Python code right in the textbook.",
        id: "sixth",
        next: "seventh"
    });

    guiders.createGuider({
        attachTo: "#codeexample1_code_div",
        highlight: "#codeexample1_code_div",
        overlay: true,
        title: "Code Editor",
        description: "Write and edit code in this text window...",
        id: "seventh",
        next: "eighth"
    });

    guiders.createGuider({
        attachTo: "#codeexample1_runb",
        highlight: "#codeexample1_runb",
        overlay: true,
        title: "Code Editor",
        description: "...and then click the 'Run' button to execute your code.",
        id: "eighth",
        next: "ninth"
    });
}

setup();
