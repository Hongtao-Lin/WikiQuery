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
  componentDidMount() {
    $('select').material_select();
  },
	render : function(){
		return(
			<div>
			  <form className="input-field col s12" onSubmit={this.handleSubmit}>
			    <select>
			      <option value="" disabled selected>Choose your option</option>
			      <option value="1">Find me the hierarchies on this entity</option>
			      <option value="2">Find me the entities that co-occurred with it</option>
			      <option value="3">Find me the properties and statements about it</option>
			    </select>
			    <label>Query Select</label>
			    <input type="submit" value="Submit" className="waves-effect waves-light btn" />
			  </form>
			</div>
		)
	}
});

module.exports = MessageForm;


