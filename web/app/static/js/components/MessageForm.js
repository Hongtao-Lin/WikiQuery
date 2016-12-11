var React = require("react");

var MessageForm = React.createClass({
  getInitialState : function(){
  	return {
  		value: ''
  	}
  },
  handleChange(e) {
    this.setState({value: e.target.value});
  },
  handleSubmit(e) {
	// var content = this.refs.content.getDOMNode().value.trim();
	this.props.submitMessage(this.state.value);
	e.preventDefault();
  },
	render : function(){
		return(
		<div className="row">
			<h5>Search an entity by its name:</h5>
		    <form className="col s12" onSubmit={this.handleSubmit}>
		      <div className="row">
		        <div className="input-field col s12">
		          <input id="entity" type="text" className="validate" value={this.state.value} onChange={this.handleChange}/>
		          <label htmlFor="entity">English charcaters only</label>
		        </div>
		      </div>
		      <input type="submit" value="Submit" className="waves-effect waves-light btn" />
		    </form>
		  </div>
		)
	}
});

module.exports = MessageForm;




