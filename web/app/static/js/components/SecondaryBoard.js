var React = require("react");
var ReactDOM = require("react-dom");


var queryHeader = [
	{"id": "Entity ID", "name": "Name", "desc": "Description"},
	{"id": "Entity ID", "name": "Name", "desc": "Description"},
	{"pname": "Property Name", "pvalue": "Property Value", "qname": "Qualifier Name", "qvalue": "Qualifier Value"},
]


var CustomMessage = React.createClass({
	render : function(){
		var msg = this.props.message;
		var header = queryHeader[this.props.qtype-1];
		var handleClick = this.handleClick;
		// console.log(this.props);
		// console.log(this.props.qtype);
		// console.log(this.props.qtype-1);
		// console.log(queryHeader);
		styles = {
			"cursor": "pointer"
		};
		selected_styles = {
			"cursor": "pointer",
			"backgroundColor": "rgba(0,128,128,0.2)"
		}
		return(
			<table className="highlight">
        <thead>
          <tr>
      {Object.keys(header).map(function(key, idx) {
      	return (
      		<th data-field={key} key={idx}>{header[key]}</th>
      	)
      })}
          </tr>
        </thead>
        <tbody>
			{msg.map(function(item, i){
				return (
					<tr key={i}>
						{item.map(function(col, j) {
							return <td key={j}>{col}</td>;
						})}
					</tr>
				);
			})}
        </tbody>
      </table>
		)
	}
});

var SecondaryBoard = React.createClass({
  getInitialState : function(){
  	return {
  		qtype: "",
  		data: []
  	}
  },
	submitSecondaryMessage : function (eid, qtype) {
		$.ajax({
			type:'post',
			url:'/secondary_query',
			data:{eid: eid, qtype: qtype}
		}).done(function (res) {
			this.setState({
				qtype: parseInt(this.state.qtype),
				data: res.data
			});

		}.bind(this));
	},
  handleSubmit(e) {
		// var content = this.refs.content.getDOMNode().value.trim();
		this.submitSecondaryMessage(this.props.eid, this.state.qtype);
		e.preventDefault();
  },
  componentDidMount() {
  	var element = ReactDOM.findDOMNode(this.refs.dropdown);
  	var ele = this;
    $(element).material_select();
  	$(element).on('change',function(){
	    ele.setState({
	    	qtype: parseInt($(this).val()),
	    	data: []
	    });
  	});

  },
  componentWillReceiveProps : function(nextProps) {
  	if (nextProps.eid != this.props.eid) {
  		this.setState({
  			qtype: this.state.qtype,
  			data: []
  		})
  	}
  },
  shouldComponentUpdate : function(nextProps, nextState) {
  	console.log(this.state.data)
  	console.log(nextState.data)
  	var isSame = (this.state.data == nextState.data)
  	console.log(isSame)
  	// var isSame = (this.state.qtype == nextState.qtype) && (this.props.eid == nextProps.eid)
  	return !isSame
  },
	render : function(){
		var qtype = this.state.qtype;
		return(
			<div>
			  <form 
			  	id="secondary_form" 
			  	className="input-field col s12"
			  	onSubmit={this.handleSubmit}>
			    <select 
			    	ref="dropdown" 
			    	defaultValue="" >
			      <option value="" disabled>Choose your option</option>
			      <option value="1">Find me the precedent categories it belongs to</option>
			      <option value="2">Find me the entities that co-occurred with it</option>
			      <option value="3">Find me the properties and statements about it</option>
			    </select>
			    <label>Query Select</label>
			    <input 
			    	type="submit" 
			    	value="Submit" 
			    	className="waves-effect waves-light btn" 
			    	/>
			    {this.state.data.length>0 &&
			    	 <CustomMessage qtype={this.state.qtype} message={this.state.data}/>
			    }
			  </form>
			</div>
		);
	}
});

module.exports = SecondaryBoard;


