var ws = null;
function connect(event) {
    ws = new WebSocket(`${eBookConfig.websocketUrl}/chat/${user}/ws`);
    messageTrail = {};
    if (ws) {
        console.log(`Websocket Connected: ${ws}`);
    }

    ws.onclose = function () {
        alert("You have been disconnected from the peer instruction server. Will Reconnect.")
        connect();
    };

    ws.onmessage = function (event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        message.classList.add("incoming-mess")
        let mess = JSON.parse(event.data);
        if (mess.type === "text") {
            if (!(mess.time in messageTrail)) {
                var content = document.createTextNode(`${mess.from}: ${mess.message}`)
                message.appendChild(content)
                messages.appendChild(message)
                messageTrail[mess.time] = mess.message;
            }
        } else if (mess.type === "control") {
            let messarea;
            switch (mess.message) {
                // This will be some kind of control message for the page
                case "countDownAndStop":
                    messarea = document.getElementById("imessage");
                    let count = 10;
                    let itimerid = setInterval(async function () {
                        if (count > 0) {
                            messarea.innerHTML = `<h3>Finish Up only ${count} seconds remaining</h3>`;
                            count = count - 1;
                        } else {
                            messarea.innerHTML = `<h3>Please Give an explanation for your answer</h3><p>Then discuss your answer with your partner</p>`;
                            window.mcList[currentQuestion].submitButton.disabled = true;
                            window.mcList[currentQuestion].disableInteraction();
                            clearInterval(itimerid);
                            // Get the current answer and insert it into the 
                            let ansSlot = document.getElementById("first_answer");
                            let currAnswer = window.mcList[currentQuestion].answer;
                            const ordA = 65;
                            currAnswer = String.fromCharCode(ordA + parseInt(currAnswer));
                            ansSlot.innerHTML = currAnswer;
                            // send log message to indicate voting is over
                            if (typeof voteNum !== "undefined" && voteNum == 2) {
                                await logStopVote();
                            }
                        }
                    }, 1000);
                    break;
                case "enableVote":
                    window.mcList[currentQuestion].submitButton.disabled = false;
                    window.mcList[currentQuestion].enableInteraction()
                    messarea = document.getElementById("imessage");
                    messarea.innerHTML = `<h3>Time to make your 2nd vote</h3>`
                    break;
                case "enableNext":
                    let butt = document.getElementById("nextqbutton");
                    if (butt) {
                        butt.removeAttribute("disabled")
                    }
                    break;
                case "enableChat":
                    let discPanel = document.getElementById("discussion_panel");
                    if (discPanel) {
                        discPanel.style.display = "block";
                    }
                    let pnameSlot = document.getElementById("pname");
                    let panswerSlot = document.getElementById("panswer");
                    pnameSlot.innerHTML = mess.from;
                    const ordA = 65;
                    let currAnswer = String.fromCharCode(ordA + parseInt(mess.answer));
                    panswerSlot.innerHTML = currAnswer;
                    break;
                default:
                    console.log("unknown control message");
            }
        }
    }

    window.onbeforeunload = function () {
        ws.onclose = function () { }; // disable onclose handler first
        ws.close();
    };
}

async function logStopVote() {
    // This can be refactored to take some parameters if peer grows
    // to require more logging functionality.
    let headers = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let eventInfo = {
        sid: eBookConfig.username,
        div_id: currentQuestion,
        event: "peer",
        act: "stop_question",
        course: eBookConfig.course,
    }
    let request = new Request(eBookConfig.ajaxURL + "hsblog", {
        method: "POST",
        headers: headers,
        body: JSON.stringify(eventInfo),
    });
    try {
        let response = await fetch(request);
        if (!response.ok) {
            throw new Error("Failed to save the log entry");
        }
        post_return = response.json();
    } catch (e) {
        alert(`Error: Your action was not saved! The error was ${e}`);
        console.log(`Error: ${e}`);
    }
}
// Send a message to the websocket server
// the server can then broadcast the message or send it to a
// specific user
async function sendMessage(event) {
    var input = document.getElementById("messageText")
    //#ws.send(JSON.stringify(mess))
    let mess = {
        type: "text",
        from: `${user}`,
        message: input.value,
        time: Date.now(),
        broadcast: false,
        course_name: eBookConfig.course,
        div_id: currentQuestion
    };
    await publishMessage(mess)
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    message.classList.add("outgoing-mess")
    var content = document.createTextNode(input.value)
    message.appendChild(content)
    messages.appendChild(message)
    input.value = ''
    // not needed for onclick event.preventDefault()
}

function warnAndStopVote(event) {
    let mess = {
        type: "control",
        sender: `${user}`,
        message: "countDownAndStop",
        broadcast: true
    }

    publishMessage(mess);
    if (event.srcElement.id == "vote1") {
        let butt = document.querySelector("#vote1")
        butt.classList.replace("btn-info", "btn-secondary")
    } else {
        let butt = document.querySelector("#vote3")
        butt.classList.replace("btn-info", "btn-secondary")

    }
}

async function makePartners() {
    let butt = document.querySelector("#makep")
    butt.classList.replace("btn-info", "btn-secondary")

    let data = {
        div_id: currentQuestion,
        start_time: startTime, // set in dashboard.html when loaded
    }
    let jsheaders = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let request = new Request("/runestone/peer/make_pairs", {
        method: "POST",
        headers: jsheaders,
        body: JSON.stringify(data),
    });
    let resp = await fetch(request);
    let spec = await resp.json();
}

function startVote2(event) {
    let butt = document.querySelector("#vote2")
    butt.classList.replace("btn-info", "btn-secondary")
    voteNum += 1;
    startTime2 = new Date().toUTCString();
    let mess = {
        type: "control",
        sender: `${user}`,
        message: "enableVote",
        broadcast: true
    }
    //ws.send(JSON.stringify(mess));
    publishMessage(mess)

}

async function clearPartners(event) {

    let butt = document.querySelector("#clearp")
    butt.classList.replace("btn-info", "btn-secondary")

    let data = {
        div_id: currentQuestion
    }
    let jsheaders = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let request = new Request("/runestone/peer/clear_pairs", {
        method: "POST",
        headers: jsheaders,
        body: JSON.stringify(data),
    });
    let resp = await fetch(request);
    let spec = await resp.json();
}

function enableNext() {
    let mess = {
        type: "control",
        sender: `${user}`,
        message: "enableNext",
        broadcast: true
    }
    publishMessage(mess);
    return true;
}

async function publishMessage(data) {
    let jsheaders = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let request = new Request("/runestone/peer/publish_message", {
        method: "POST",
        headers: jsheaders,
        body: JSON.stringify(data),
    });
    let resp = await fetch(request);
    let spec = await resp.json();
}


async function ratePeer(radio) {
    let jsheaders = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let eventInfo = {
        sid: eBookConfig.username,
        div_id: currentQuestion,
        event: "ratepeer",
        course_id: eBookConfig.course,
        rating: radio.value,
    }
    let request = new Request("/runestone/peer/log_peer_rating", {
        method: "POST",
        headers: jsheaders,
        body: JSON.stringify(eventInfo),
    });
    try {
        let response = await fetch(request);
        if (!response.ok) {
            throw new Error("Failed to save the log entry");
        }
        post_return = response.json();
    } catch (e) {
        alert(`Error: Your action was not saved! The error was ${e}`);
        console.log(`Error: ${e}`);
    }
}

$(function () {
    let tinput = document.getElementById("messageText");
    if (tinput) {
        tinput.addEventListener("keyup", function (event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                document.getElementById("sendpeermsg").click();
            }
        });
    }
});

