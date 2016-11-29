module.exports = {
    entry : {
        index : "./index.js"
    },
    output : {
        path : "./build",
        filename : "bundle.js"
    },
    module : {
        loaders :[
            {test:/\.js$/, loader:'jsx-loader'},
            {test:/\.scss$/, loader:['style','css','sass']}
        ]

    }
}