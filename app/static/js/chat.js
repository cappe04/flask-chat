class Chat {
    constructor(socket){
        this.socket = socket
        
        this.chat = $("#chat")
        this.inputMessage = $("#input_message")
        this.buttonSend = $("#btn_send")
        this.buttonLoad = $("#btn_load")

        this.loadIndicator = $('<div class="loading">Loading more messages...</div>')
        this.emptyIndicator = $('<div class="loading">No more messages...</div>')

        this.offset = 0

        // Idk wtf this is but ChatGPT told me to do it
        this.onNew = this.onNew.bind(this);
        this.onLoad = this.onLoad.bind(this);
        this.send = this.send.bind(this);
        this.get = this.get.bind(this);
        this.scrollHandler = this.scrollHandler.bind(this);

        this.socket.on("message:new", this.onNew)
        this.socket.on("message:load", this.onLoad)

        this.chat.on("scroll", this.scrollHandler)
        this.buttonSend.click(this.send)
        this.buttonLoad.click(this.get)

        this.chat.prepend(this.loadIndicator)
    }
    
    onNew(message){
        var html = this.renderMessage(message)
        this.chat.append(html)
        this.offset++
        var height = this.chat.prop("scrollHeight")
        this.chat.scrollTop(height)
    }

    onLoad(messages){
        this.loadIndicator.remove()
        if(messages == undefined){
            this.chat.prepend(this.emptyIndicator)
            return
        }
        var preLoadHeight = this.chat.prop("scrollHeight")
        for(var message of messages){
            var html = this.renderMessage(message)
            this.chat.prepend(html)
            this.offset++
        }
        var postLoadHeight = this.chat.prop("scrollHeight")
        this.chat.scrollTop(postLoadHeight- preLoadHeight)
    }

    send(){
        this.socket.emit("message:send", {
            "message": this.inputMessage.val()
        })
        this.inputMessage.val("")
    }

    get(){
        this.socket.emit("message:get", {
            "offset": this.offset
        })
    }

    scrollHandler(){
        this.chat.prepend(this.loadIndicator)
        if(this.chat.scrollTop() === 0){
            this.get()
        }
    }

    renderMessage(message){
        var html = `
        <div class=message data-id=${message.message_id}>
            <strong>${message.username}</strong>: ${message.message} (<i>${message.timestamp}</i>)
        </div>
        `
        return html
    }
}

$("document").ready(function(){
    socket = io.connect(document.location.origin)

    const chat = new Chat(socket)

    socket.on("connect", function(){
        chat.get()
    })


    socket.on("page:reload", function(){
        console.log("Something went wrong, reloading page!")
        location.reload()
    })

    $("#btn_home").click(function(){
        document.location.assign(document.location.origin + "/home")
    })
})