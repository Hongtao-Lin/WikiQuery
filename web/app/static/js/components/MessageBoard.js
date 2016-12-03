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
			prompt: ""
		}
	},
	setEntityID : function(eid) {
		this.setState({
			entity_list: this.state.entity_list,
			eid: eid,
			prompt: ""
		});
	},
	submitMessage : function (val) {
		this.setState({
			eid: "",
			entity_list: [],
			prompt: ""
		});
		$("#first_loading").addClass("progress");
		$.ajax({
			type:'post',
			url:'/find_entity',
			data:{sent:val}
		}).done(function (res) {
			$("#first_loading").removeClass("progress");
			if (res.status == "fail") {
				$("#error_msg").text(res.prompt);
				$("#error_modal").modal('open');
			}
			this.setState({
				eid: this.state.eid,
				entity_list: res.data,
				prompt: res.prompt 
			});
		}.bind(this));
	},
	render : function(){
		return(
			<div className="container">
				<MessageForm submitMessage={this.submitMessage}/>
			  	<div className="" id="first_loading">
					<div className="indeterminate"></div>
				</div>  		
				{this.state.entity_list.length>0 &&
					<Message message={this.state.entity_list} setEntityID={this.setEntityID}/>
				}
				{this.state.eid != "" &&
					<SecondaryBoard eid={this.state.eid}  />
				}
			</div>
		)
	}
});

module.exports = MessageBoard;
