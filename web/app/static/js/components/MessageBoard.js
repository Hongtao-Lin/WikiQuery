var React = require("react");
var NERInfo = require("./NERInfo");
var Message = require("./Message");
var MessageForm = require("./MessageForm");
var SecondaryForm = require("./SecondaryForm");

var MessageBoard = React.createClass({
	getInitialState : function(){
		return {
			entity_list: [],
			entity_selected: "",
			second_list: [],
		}
	},
	setEntityID : function(val) {
		this.setState({
			entity_selected: val
		});
	},
	submitMessage : function (val) {
		$.ajax({
			type:'post',
			url:'/find_entity',
			data:{sent:val}
		}).done(function (res) {
			entity_list = res.data
			this.setState({
				entity_list: res.data,
				ner_type: ""
			});

		}.bind(this));
	},
	submitSecondaryMessage : function (val) {
		url_route = [
			'/find_tree',
			'/find_related',
			'/find_prop'
		];
		eid = this.state.entity_selected;
		console.log(eid)
		$.ajax({
			type:'post',
			url:url_route[parseInt(val)],
			data:{eid:eid}
		}).done(function (res) {
			items = this.state
			this.setState({
				second_list: res.data,
			});

		}.bind(this));
	},
	render : function(){
		if (this.state.second_list.length) {
				<div>
	        <h4>Let's get some entities first!</h4>
					<MessageForm submitMessage={this.submitMessage}/>
					<div>
						<Message message={this.state.entity_list} setEntityID={this.setEntityID}/>
					</div>
					<h4>How about knowing more about the selected entity?</h4>
					<SecondaryForm submitMessage={this.submitSecondaryMessage}/>
					<div>
						<Message message={this.state.second_list}/>
					</div>
				</div>
		}
		if (this.state.entity_list.length) {
			return(
				<div>
	        <h4>Let's get some entities first!</h4>
					<MessageForm submitMessage={this.submitMessage}/>
					<div>
						<Message message={this.state.entity_list}/>
					</div>
					<h4>How about knowing more about the selected entity?</h4>
					<SecondaryForm submitMessage={this.submitSecondaryMessage}/>
				</div>
			)
		} else {
			return(
				<div>
			        <h4>Let's get some entities first!</h4>
					<MessageForm submitMessage={this.submitMessage}/>
				</div>
			)
		}
	}
});

module.exports = MessageBoard;
