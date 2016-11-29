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
  	console.log(this.state.value);
		// var content = this.refs.content.getDOMNode().value.trim();
		this.props.submitMessage(this.state.value);
		e.preventDefault();
  },
	render : function(){
		return(

			<div className="row">
		    <form className="col s12" onSubmit={this.handleSubmit}>
		      <div className="row">
		        <div className="input-field col s12">
		          <input id="entity" type="text" className="validate" value={this.state.value} onChange={this.handleChange}/>
		          <label for="entity">Describe the name of entity</label>
		        </div>
		      </div>
		      <input type="submit" value="Submit" className="waves-effect waves-light btn" />
		    </form>
		  </div>
		)
	}
});

module.exports = MessageForm;




