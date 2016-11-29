var React = require("react");
var MessageBoard = require("./components/MessageBoard");

$(document).ready(function () {

  // React.render(<App />, document.body);
	React.render(<MessageBoard/>,document.getElementById("message-board-container"));
    $('select').material_select();
});
