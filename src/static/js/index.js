// maybe encrpyt user_id with secret key from server when sendnig it

$(document).ready(() => {
    console.log("Hej")
    var socket = io.connect("http://localhost:5000");

    socket.on("connect", () => {
        socket.emit("event", { message: "hej" })
    })
    
    socket.on("response", (response) => {
        console.log(response)
    })

})