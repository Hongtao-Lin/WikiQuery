var React = require("react");


var MessageBlock = React.createClass({
	render : function() {
		var msg = this.props.msg;
		var eid = msg[0];
		var name = msg[1];
		var desc = msg[2];
		return (
				<tr>
					<td>eid</td>
					<td>name</td>
					<td>desc</td>
				</tr>
			) 
	}
});

var Message = React.createClass({
	handleClick: function(eid) {
		this.props.setEntityID(eid);
	},
	render : function(){
		var msg = this.props.message;
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
						return <MessageBlock data-tag={item[0]} key={item.id} msg={item[idx]} \
							onclick={this.handleClick.bind(null, item[0])}/>
					})}
          
        </tbody>
      </table>
		)
	}
});

module.exports = Message;
