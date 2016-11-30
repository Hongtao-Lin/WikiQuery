var React = require("react");
var ReactDOM = require("react-dom");

var Message = React.createClass({
	getInitialState : function(){
		return {
			select_id: ""
		}
	},
	componemtWillReceiveProps: function() {
		this.setState({
			select_id : ""
		})
	},
	handleClick : function(eid) {
		if (this.state.select_id == eid) {
			this.setState({select_id: ""});
		} else {
			this.setState({select_id: eid});
		}
		this.props.setEntityID(eid);
	},
	render : function(){
		var msg = this.props.message;
		var setEntityID = this.props.setEntityID;
		var select_id = this.state.select_id;
		var handleClick = this.handleClick;
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
              <th data-field="id">Entity ID</th>
              <th data-field="name">Name</th>
              <th data-field="price">Description</th>
          </tr>
        </thead>
        <tbody>
			{msg.map(function(item, idx){
				return (
					<tr 
						style={select_id==item[0]? selected_styles : styles}
						onClick={handleClick.bind(null, item[0])}
						key={idx}>
						<td>{item[0]}</td>
						<td>{item[1]}</td>
						<td>{item[2]}</td>
					</tr>
				)
			})}
        </tbody>
      </table>
		)
	}
});

module.exports = Message;

