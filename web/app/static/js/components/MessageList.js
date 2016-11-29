var React = require("react");
var Message = require("./Message");

var MessageList = React.createClass({
    render : function () {
        var messages = this.props.messages.map(function(item){
            return <Message message={item}/>
        });
        return(
            <div>
                {messages}
            </div>
        )
    }
});

module.exports = MessageList;