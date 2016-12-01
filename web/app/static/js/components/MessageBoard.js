var React = require("react");
var ReactDOM = require("react-dom");
var MessageForm = require("./MessageForm");
var Message = require("./Message");
var SecondaryBoard = require("./SecondaryBoard");

var MessageBoard = React.createClass({
	getInitialState : function(){
		return {
			entity_list: [],
			eid: "",
		}
	},
	setEntityID : function(eid) {
		this.setState({
			entity_list: this.state.entity_list,
			eid: eid
		});
	},
	submitMessage : function (val) {
		$.ajax({
			type:'post',
			url:'/find_entity',
			data:{sent:val}
		}).done(function (res) {
			if (res.status == "fail") {
				$("first_error_msg").text(res.data);
				$("first_error_modal").modal('open');
			} else {
				this.setState({
					eid: this.state.eid,
					entity_list: res.data 
				});
			}
		}.bind(this));
	},
	render : function(){
		return(
			<div>
		        <h5>Search an entity by its name:</h5>
				<MessageForm submitMessage={this.submitMessage}/>
				{this.state.entity_list.length>0 &&
					<Message message={this.state.entity_list} setEntityID={this.setEntityID}/>
				}
				{this.state.eid != "" &&
					[<h5 key="0">Know more about the selected entity:</h5>,
					<SecondaryBoard key="1" eid={this.state.eid}  />]
				}
			</div>
		)
	}
});

module.exports = MessageBoard;
