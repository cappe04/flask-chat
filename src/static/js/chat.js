$("document").ready(function(){
    socket = io.connect(document.location.origin)

    // socket.on("connect", function(){
    //     socket.emit("user_connect")
    // })
    
    const channel_id = parseInt(document.location.pathname.slice(-1))

    socket.on("connect", function(){
        socket.emit("client_connect", {
            "channel_id": channel_id
        })
    })

    socket.on("refresh", function(){
        console.log("Something went wrong, reloading page!")
        location.reload()
    })

    socket.on("server_send_message", function(data){
        var message = JSON.parse(data)
        $("#chat").append(
            `<div class=message data-id=${message.message_id}>
            <strong>${message.username}</strong>: ${message.message} (<i>${message.timestamp}</i>)
            </div>`
        )
        console.log(data)
    })

    $("#btn_send").click(function(){
        socket.emit("client_send_message", {
            "message": $("#input_message").val(),
            "channel_id": channel_id
        })
    })

    $("#btn_home").click(function(){
        document.location.assign(document.location.origin + "/home")
    })
})