var React = require("react");
var ReactDOM = require("react-dom");

var parser = new Parser('en');

var NLQBoard = React.createClass({
	getInitialState : function(){
		return {
			answer: "",
			query: "",
			prompt: ""
		}
	},
  handleChange(e) {
    this.setState({query: e.target.value});
  },
  handleSubmit(e) {
	// var content = this.refs.content.getDOMNode().value.trim();
	this.submitMessage(this.state.query);
	e.preventDefault();
  },
	submitMessage : function (val) {
		var _this = this;
		// console.log(val);
		$("#nlq_loading").addClass("progress");
		parser.parseQuestion(val)
		.then(function(parsed) {
			$("#second_loading").removeClass("progress");
			$.ajax({
				type:'post',
				url:'/nlq_ask',
				data:{args:JSON.stringify(parsed)}
			}).done(function (res) {
				if (res.status == "fail") {
					$("#error_msg").text(res.prompt);
					$("#error_modal").modal('open');
				}
				this.setState({
					query: this.state.query,
					answer: res.data ,
					prompt: ""
				});
			}.bind(_this));
		}, function() {
			console.log("Error!")
		});
	},
	render : function(){
		return(
			<div>
		        <h5>Say something:</h5>
				<div className="row">
			    <form className="col s12" onSubmit={this.handleSubmit}>
			      <div className="row">
			        <div className="input-field col s12">
			          <input 
			          	id="query" 
			          	type="text" 
			          	className="validate" 
			          	value={this.state.query} 
			          	onChange={this.handleChange}/>
			          <label htmlFor="query">English charcaters only</label>
			        </div>
			      </div>
			    <input type="submit" value="Submit" className="waves-effect waves-light btn" />
			    </form>
			    </div>
				{this.state.answer != "" &&
					[<i className="material-icons medium">label_outline</i>,
					<div className="col s12" id="nlq_div">
						<p className="z-depth-3" id="nlq_answer">
						{this.state.answer}
						</p>
					</div>]
				}
		  </div>
		)
	}
});

module.exports = NLQBoard;
