var React = require("react");

var	dict = {"PER": ["12"], "LOC": [], "ORG": []};

var DisplayDict = React.createClass({
	render: function() {
		var p = this;
		var dict = this.props.dict;
		return (
			<ul className="addDictList">
				{Object.keys(dict).map(function(tag) {
					return (dict[tag].map(function(d, i) {
						return (<li className={`tag ${"format-"+tag}`}>{d}
							<span className="del-btn" onClick={p.props.delWord.bind(this, tag, i)}></span>
						</li>)
					}))
				})}
			</ul>
		)
	}
});

var DictContainer = React.createClass({
	getInitialState: function() {
		return {
			inputText: "",
			dict: dict
		};
	},
	submitDict: function() {
		$.ajax({
			type:'post',
			url:'/addDict',
			data:{dict:JSON.stringify(dict)}
		});
	},
	processInput: function(e) {
		if (e.key == "Enter") {
			var tempDict = this.state.dict;
			text = e.target.value.trim();
			text.split(";").map(function(s) {
				tempDict[s.split(":")[1].trim()].push(s.split(":")[0].trim());
			})
			this.setState({dict: tempDict});
			console.log(this.state.dict);
			this.setState({inputText: ""});
		}
	},
	addText: function(e) {
		this.setState({inputText: e.target.value})
	},
	delWord: function(tag, i) {
		var tempDict = this.state.dict;
		tempDict[tag].splice(i,1);
		this.setState({dict: tempDict});
	},
	render: function() {
		return (
			<div>
				<p>HIHIHI</p>
				<input type="text" placeholder="Input your words :)" value={this.state.inputText} onKeyPress={this.processInput} onChange={this.addText}/> 
				<DisplayDict dict={this.state.dict} delWord={this.delWord} />
				<input type="submit" value="Submit" onClick={this.submitDict} />
			</div>
		);
	}
});


module.exports = DictContainer;