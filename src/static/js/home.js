$("document").ready(function(){

    $("#btn_join_channel").click(function(){
        var channel_id = $("#dropdown_channels").val();
        document.location.assign(document.location.origin + "/chat/" + channel_id)
    })
})