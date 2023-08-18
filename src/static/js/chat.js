$("document").ready(function(){
    socket = io.connect(document.location.origin)

    // socket.on("connect", function(){
    //     socket.emit("user_connect")
    // })
    
    const channel_id = document.location.pathname.slice(-1)

    socket.on("connect", function(){
        socket.emit("user_connect", {
            "channel_id": channel_id
        })
    })

    socket.on("user_connected", function(data){
        console.log("user_connected")
        console.log(data)
    })

    socket.on("server_send_message", function(data){
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