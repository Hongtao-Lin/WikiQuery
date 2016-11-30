var React = require("react");
var ReactDOM = require("react-dom");

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
		$.ajax({
			type:'post',
			url:'/nlq_ask',
			data:{query:val}
		}).done(function (res) {
			this.setState({
				query: this.state.query,
				answer: res.data 
			});
		}.bind(this));
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
