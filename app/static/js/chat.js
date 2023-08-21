const channel_id = parseInt(document.location.pathname.slice(-1))
let offset = 0

function render_message(message, insert=false){
    offset++;
    html = `<div class=message data-id=${message.message_id}>
    <strong>${message.username}</strong>: ${message.message} (<i>${message.timestamp}</i>)
    </div>`

    if(insert)
        $("#chat").prepend(html)
    else
        $("#chat").append(html)
}

$("document").ready(function(){
    socket = io.connect(document.location.origin)

    socket.on("connect", function(){
        socket.emit("client:connect", {
            "channel_id": channel_id
        })
        socket.emit("message:get", {
            "channel_id": channel_id,
            "offset": offset
        })
    })

    socket.on("page:reload", function(){
        console.log("Something went wrong, reloading page!")
        location.reload()
    })

    socket.on("message:new", function(message){
        render_message(message)
        console.log(message)
    })

    socket.on("message:load", function(messages){
        if (messages == undefined){
            console.log("There are no more messages to load!")
            return
        }
        for(message of messages){
            render_message(message, true)
        }
    })

    $("#btn_send").click(function(){
        socket.emit("message:send", {
            "message": $("#input_message").val(),
            "channel_id": channel_id
        })
    })

    $("#btn_load").click(function(){
        socket.emit("message:get", {
            "channel_id": channel_id,
            "offset": offset
        })
    })

    $("#btn_home").click(function(){
        document.location.assign(document.location.origin + "/home")
    })
})