
// function getCookie(cookie){
//     if(document.cookie.includes(cookie)){
//         console.log(document.cookie + ";")
//         console.log((document.cookie + ";").match(`${cookie}=(.*?);"`))
//         return (document.cookie + ";").match(`${cookie}=(.*?);"`)[1];
//     }
//     return null;
// }


$("document").ready(function(){
    socket = io.connect(document.location.origin)

    // socket.on("connect", function(){
    //     socket.emit("user_connect")
    // })

    // socket.on("user_connected", function(data){
    //     console.log(data)
    // })

    socket.on("server_send_message", function(data){
        console.log(data)
    })

    $("#btn_send").click(function(){
        socket.emit("client_send_message", {
            "message": $("#input_message").val()
        })
    })

})