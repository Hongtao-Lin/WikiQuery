var React = require("react");


var NERInfo = React.createClass({
	render : function(){
		// var type = this.props.ner_type;
		var type = ["PER", "LOC", "ORG"];
		var spanStyle = {
			marginRight: '7px'
		};
		var display = type.map(function(item) {
			if (item != "o") {
				ne_type = item;
			return (
				[<span className={`tag ${"format-"+ne_type}`} style={spanStyle}>{ne_type}</span>]
			)}
		});
		return(
			<div>
				{display}
			</div>
		)
	}
});

module.exports = NERInfo;