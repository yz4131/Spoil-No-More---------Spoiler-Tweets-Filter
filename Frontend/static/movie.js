async function fetchMovie() {
    let tweet = await fetch("https://2hjlk03e01.execute-api.us-east-1.amazonaws.com/v1/get_stream?q=movie")
    .then(response=>response.text())
    .then(data=>data)
    console.log(tweet)
    if (tweet == "Not Found") {
        let tweet = await fetchMovie()
    }
    return tweet
}

async function streaming() {
    if (stream == true) {
        let tweet = JSON.parse(await fetchMovie())
        console.log(tweet["data"])
        console.log(tweet["labels"])
        let content = $("<div>").text(tweet["data"])
        content.addClass("row content")
        $("#all").prepend(content)
        if (tweet["labels"] == 0) {
            let content_f = $("<div>").text(tweet["data"])
            content_f.addClass("row content")
            $("#filtered").prepend(content_f)
        }
    }
}

function stopStreaming() {
    $("#streaming_switch").empty()
    let button = $("<button>").text("Start Streaming")
    button.attr("id", "switch_button")
    $("#streaming_switch").append(button)
    $("#switch_button").click(function(){
        startStreaming()
    })
    stream = false
}

function startStreaming() {
    $("#streaming_switch").empty()
    let button = $("<button>").text("Stop Streaming")
    button.attr("id", "switch_button")
    $("#streaming_switch").append(button)
    $("#switch_button").click(function(){
        stopStreaming()
    })
    stream = true
    setInterval(function(){streaming()}, 3000)
}

$(document).ready(function(){
    var stream = true
    $("#switch_button").click(function(){
        startStreaming()
    })
})