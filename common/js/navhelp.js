/**
 * Created by isaacdontjelindell on 8/2/13.
 */

/* Sets up the interactive navhelp */

function setup() {
    guiders.createGuider({
        buttons: [{name: "Next"}],
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
        attachTo: "#codeexample1 .ac_caption",
        highlight: "#codeexample1 .ac_caption",
        title: "ActiveCode Blocks",
        description: "ActiveCode blocks allow you to write and execute Python code right in the textbook.",
        id: "sixth",
        next: "seventh"
    });

    guiders.createGuider({
        attachTo: "#codeexample1_code_div",
        highlight: "#codeexample1_code_div",
        overlay: true,
        title: "ActiveCode Editor",
        description: "Write and edit code in this text window...",
        id: "seventh",
        next: "eighth"
    });

    guiders.createGuider({
        attachTo: "#codeexample1_runb",
        highlight: "#codeexample1_runb",
        overlay: true,
        title: "ActiveCode Editor",
        description: "...and then click the 'Run' button to execute your code.",
        id: "eighth",
        next: "ninth"
    });

    guiders.createGuider({
        attachTo: "#codeexample1_saveb",
        highlight: "#codeexample1_saveb",
        overlay: true,
        title: "ActiveCode Blocks",
        description: "If you are logged in, you can save your code, and then load again later.",
        id: "ninth",
        next: "tenth"
    });

    guiders.createGuider({
        attachTo: "#firstexample",
        highlight: "#firstexample",
        offset: {left: -375, top:0},
        title: "CodeLens",
        description: "The CodeLens visualizer allows you to execute some code step-by-step, and see the values of all the variables and objects as they are executed.",
        id: "tenth",
        next: "eleventh"
    });

    guiders.createGuider({
        attachTo: "#firstexample #jmpStepFwd",
        highlight: "#firstexample #jmpStepFwd",
        overlay: true,
        title: "CodeLens Controls",
        description: "Use these buttons below the code window to control how you step through the code.",
        id: "eleventh",
        next: "twelfth"
    });

    guiders.createGuider({
        attachTo: "#question1_1",
        highlight: "#question1_1",
        overlay: true,
        title: "Self-Check Questions",
        description: "These questions allow you to check your understand as you move through the textbook.",
        id: "twelfth",
        next: "thirteenth"
    });

    guiders.createGuider({
        attachTo: "#question1_1 button[name='do answer']",
        highlight: "#question1_1 button[name='do answer']",
        overlay: true,
        title: "Self-Check Questions",
        description: "Click this button to get feedback on your answer(s).",
        id: "thirteenth",
        next: "fourteenth"
    });

    guiders.createGuider({
        attachTo: "#question1_1 button[name='compare']",
        highlight: "#question1_1 button[name='compare']",
        overlay: true,
        title: "Self-Check Questions",
        description: "Click this button to get see how you are doing in relation to other people using the textbook.",
        id: "fourteenth",
        next: "fifteenth"
    });

    guiders.createGuider({
        attachTo: ".parsons",
        highlight: ".parsons",
        overlay: true,
        title: "Parsons Problems",
        description: "Parsons exercises ask you to arrange lines of code in the correct order.",
        id: "fifteenth",
        next: "sixteenth"
    });

    guiders.createGuider({
        attachTo: "#parsons-sortableTrash-88",
        highlight: "#parsons-sortableTrash-88",
        overlay: true,
        title: "Parsons Problems",
        description: "Drag lines of code from here...",
        id: "sixteenth",
        next: "seventeenth"
    });

    guiders.createGuider({
        attachTo: "#ul-parsons-sortableCode-88",
        highlight: "#ul-parsons-sortableCode-88",
        overlay: true,
        title: "Parsons Problems",
        description: "...to here.",
        id: "seventeenth",
        next: "eighteenth"
    });

    guiders.createGuider({
        attachTo: "#feedbackLink-88",
        highlight: "#feedbackLink-88",
        overlay: true,
        title: "Parsons Problems",
        description: "Click this button to check if you've arranged the code in the correct order.",
        id: "eighteenth",
        next: "nineteenth"
    });

    guiders.createGuider({
        attachTo: "#embedded-videos img",
        highlight: "#embedded-videos img",
        overlay: true,
        title: "Embedded Videos",
        description: "To play a video embedded in the text, just click the play button.",
        id: "nineteenth",
        next: "twentieth"
    });

    guiders.createGuider({
        buttons: [{name: "Close"}],
        attachTo: "body",
        position: 0,
        overlay: true,
        title: "Thank You!",
        description: "Thanks for using this interactive textbook. ",
        id: "twentieth"
    });

}

setup();
