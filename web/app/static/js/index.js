var React = require("react");
var MessageBoard = require("./components/MessageBoard");
var NLQBoard = require("./components/NLQBoard");
var ReactDOM = require("react-dom");


$(document).ready(function () {
	url = location.href.split("/");
	url = url[url.length-1]
	if (url == "nlq") {

		ReactDOM.render(<NLQBoard/>,document.getElementById("nlq-container"));
	} else {
		ReactDOM.render(<MessageBoard/>,document.getElementById("message-board-container"));
		
	}
});
