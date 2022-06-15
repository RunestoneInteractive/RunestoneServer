var ws = null;
function connect(event) {
    ws = new WebSocket(`${eBookConfig.websocketUrl}/chat/${user}/ws`);
    messageTrail = {};
    if (ws) {
        console.log(`Websocket Connected: ${ws}`);
    }

    ws.onclose = function () {
        alert(
            "You have been disconnected from the peer instruction server. Will Reconnect."
        );
        connect();
    };

    ws.onmessage = function (event) {
        var messages = document.getElementById("messages");
        var message = document.createElement("li");
        message.classList.add("incoming-mess");
        let mess = JSON.parse(event.data);
        // This is an easy to code solution for broadcasting that could go out to
        // multiple courses.  It would be better to catch that on the server side
        // but that will take a bit more work and research
        if (mess.course_name != eBookConfig.course) {
            console.log(`ignoring message to ${mess.course_name}`);
            return;
        }
        if (mess.type === "text") {
            if (!(mess.time in messageTrail)) {
                var content = document.createTextNode(`${mess.from}: ${mess.message}`);
                message.appendChild(content);
                messages.appendChild(message);
                messageTrail[mess.time] = mess.message;
            }
        } else if (mess.type === "control") {
            let messarea;
            switch (mess.message) {
                // This will be some kind of control message for the page
                case "countDownAndStop":
                    messarea = document.getElementById("imessage");
                    let count = 5;
                    let itimerid = setInterval(async function () {
                        if (count > 0) {
                            messarea.style.color = "red";
                            messarea.innerHTML = `<h3>Finish Up only ${count} seconds remaining</h3>`;
                            count = count - 1;
                        } else {
                            messarea.style.color = "black";
                            // hide the discussion
                            let discPanel = document.getElementById("discussion_panel");
                            if (discPanel) {
                                discPanel.style.display = "none";
                            }
                            let currAnswer = window.mcList[currentQuestion].answer;
                            if (typeof currAnswer === "undefined") {
                                messarea.innerHTML = `<h3>You have not answered the question</h3><p>You will not be able to participate in any discussion unless you answer the question.</p>`;
                            } else {
                                messarea.innerHTML = `<h3>Please Give an explanation for your answer</h3><p>Then discuss your answer with your group members</p>`;
                            }
                            if (!eBookConfig.isInstructor) {
                                window.mcList[
                                    currentQuestion
                                ].submitButton.disabled = true;
                                window.mcList[currentQuestion].disableInteraction();
                            }
                            clearInterval(itimerid);
                            // Get the current answer and insert it into the
                            let ansSlot = document.getElementById("first_answer");
                            const ordA = 65;
                            if (typeof currAnswer !== "undefined") {
                                currAnswer = answerToString(currAnswer);
                                ansSlot.innerHTML = currAnswer;
                            }
                            // send log message to indicate voting is over
                            if (typeof voteNum !== "undefined" && voteNum == 2) {
                                logPeerEvent({
                                    sid: eBookConfig.username,
                                    div_id: currentQuestion,
                                    event: "peer",
                                    act: "stop_question",
                                    course: eBookConfig.course,
                                });
                            }
                        }
                    }, 1000);
                    break;
                case "enableVote":
                    window.mcList[currentQuestion].submitButton.disabled = false;
                    window.mcList[currentQuestion].submitButton.innerHTML = "Submit";
                    window.mcList[currentQuestion].enableInteraction();
                    if (typeof studentVoteCount !== "undefined") {
                        studentVoteCount += 1;
                    }
                    messarea = document.getElementById("imessage");
                    messarea.innerHTML = `<h3>Time to make your 2nd vote</h3>`;
                    $("[type=radio]").prop("checked", false);
                    break;
                case "enableNext":
                    // This moves the student to the next question in the assignment
                    let nextForm = document.getElementById("nextqform");
                    nextForm.submit();
                    break;
                case "enableChat":
                    console.log(`got enableChat message with ${mess.answer}`);
                    let discPanel = document.getElementById("discussion_panel");
                    if (discPanel) {
                        discPanel.style.display = "block";
                    }
                    let peerlist = document.getElementById("peerlist");
                    const ordA = 65;
                    adict = JSON.parse(mess.answer);
                    let peersel = document.getElementById("peersel");
                    for (const key in adict) {
                        let currAnswer = adict[key];
                        let newpeer = document.createElement("p");
                        newpeer.innerHTML = `${key} answered ${currAnswer}`;
                        peerlist.appendChild(newpeer);
                        let peeropt = document.createElement("option");
                        peeropt.value = key;
                        peeropt.innerHTML = key;
                        peersel.appendChild(peeropt);
                        peersel.addEventListener("change", function () {
                            $(".ratingradio").prop("checked", false);
                        });
                    }
                    break;
                default:
                    console.log("unknown control message");
            }
        }
    };

    window.onbeforeunload = function () {
        ws.onclose = function () {}; // disable onclose handler first
        ws.close();
    };
}

function answerToString(currAnswer) {
    const ordA = 65;
    if (currAnswer.indexOf(",") > -1) {
        let alist = currAnswer.split(",");
        let nlist = [];
        for (let x of alist) {
            nlist.push(String.fromCharCode(ordA + parseInt(x)));
        }
        currAnswer = nlist.join(",");
    } else {
        currAnswer = String.fromCharCode(ordA + parseInt(currAnswer));
    }
    console.log(`returning ${currAnswer}`);
    return currAnswer;
}

async function logPeerEvent(eventInfo) {
    // This can be refactored to take some parameters if peer grows
    // to require more logging functionality.
    let headers = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
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
    var input = document.getElementById("messageText");
    //#ws.send(JSON.stringify(mess))
    let mess = {
        type: "text",
        from: `${user}`,
        message: input.value,
        time: Date.now(),
        broadcast: false,
        course_name: eBookConfig.course,
        div_id: currentQuestion,
    };
    await publishMessage(mess);
    var messages = document.getElementById("messages");
    var message = document.createElement("li");
    message.classList.add("outgoing-mess");
    var content = document.createTextNode(input.value);
    message.appendChild(content);
    messages.appendChild(message);
    input.value = "";
    // not needed for onclick event.preventDefault()
}

function warnAndStopVote(event) {
    let mess = {
        type: "control",
        sender: `${user}`,
        message: "countDownAndStop",
        broadcast: true,
        course_name: eBookConfig.course,
    };

    publishMessage(mess);
    if (event.srcElement.id == "vote1") {
        let butt = document.querySelector("#vote1");
        butt.classList.replace("btn-info", "btn-secondary");
    } else {
        let butt = document.querySelector("#vote3");
        butt.classList.replace("btn-info", "btn-secondary");
    }
}

async function makePartners() {
    let butt = document.querySelector("#makep");
    butt.classList.replace("btn-info", "btn-secondary");
    let gs = document.getElementById("groupsize").value;
    let data = {
        div_id: currentQuestion,
        start_time: startTime, // set in dashboard.html when loaded
        group_size: gs,
    };
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
    if (!resp.ok) {
        alert(`Pairs not made ${resp.statusText}`);
    }
    let spec = await resp.json();
    if (spec !== "success") {
        alert(`Pairs not made! ${spec}`);
    }
}

function startVote2(event) {
    let butt = document.querySelector("#vote2");
    butt.classList.replace("btn-info", "btn-secondary");
    voteNum += 1;
    startTime2 = new Date().toUTCString();
    let mess = {
        type: "control",
        sender: `${user}`,
        message: "enableVote",
        broadcast: true,
        course_name: eBookConfig.course,
    };
    //ws.send(JSON.stringify(mess));
    publishMessage(mess);
}

async function clearPartners(event) {
    let butt = document.querySelector("#clearp");
    butt.classList.replace("btn-info", "btn-secondary");

    let data = {
        div_id: currentQuestion,
    };
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
        broadcast: true,
        course_name: eBookConfig.course,
    };
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
    let peerToRate = document.getElementById("peersel").value;
    let eventInfo = {
        sid: eBookConfig.username,
        div_id: currentQuestion,
        event: "ratepeer",
        peer_id: peerToRate,
        course_id: eBookConfig.course,
        rating: radio.value,
    };
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

// This function is only for use with the async mode of peer instruction
//
async function showPeerEnableVote2() {
    // Log the justification from this student
    let mess = document.getElementById("messageText").value;

    await logPeerEvent({
        sid: eBookConfig.username,
        div_id: currentQuestion,
        event: "sendmessage",
        act: `to:system:${mess}`,
        course: eBookConfig.course,
    });

    // send a request to get a peer response and display it.
    let data = {
        div_id: currentQuestion,
        course: eBookConfig.course,
    };
    let jsheaders = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let request = new Request("/runestone/peer/get_async_explainer", {
        method: "POST",
        headers: jsheaders,
        body: JSON.stringify(data),
    });
    let resp = await fetch(request);
    if (!resp.ok) {
        alert(`Error getting a justification ${resp.statusText}`);
    }
    let spec = await resp.json();
    let peerMess = spec.mess;
    let peerNameEl = document.getElementById("peerName");
    peerNameEl.innerHTML = `User ${spec.user} answered ${answerToString(spec.answer)}`;
    let peerEl = document.getElementById("peerJust");
    peerEl.innerHTML = peerMess;
    let nextStep = document.getElementById("nextStep");
    nextStep.innerHTML =
        "Please Answer the question again.  Even if you do not wish to change your answer.  After answering click the button to go on to the next question.";
    $("[type=radio]").prop("checked", false);
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
