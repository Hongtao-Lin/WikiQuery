var React = require("react");
var ReactDOM = require("react-dom");

var parser = new Parser('en');

function handleQuestion(question) {
	// parse the question
	parser.parseQuestion(question)
	.then(function(parsed) {
		handleParsed(parsed);
	}, function() {
		// the question could not be parsed
		showError(i18n.t('unparsable'));
	} );
}

var NLQBoard = React.createClass({
	getInitialState : function(){
		return {
			answer: "",
			query: "",
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
		console.log(val)
		parser.parseQuestion(val)
		.then(function(parsed) {
			console.log(parsed);
			$.ajax({
				type:'post',
				url:'/nlq_ask',
				data:{args:JSON.stringify(parsed)}
			}).done(function (res) {
				this.setState({
					query: this.state.query,
					answer: res.data 
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
					<p>{this.state.answer}</p>
				}
			</div>
		)
	}
});

module.exports = NLQBoard;
