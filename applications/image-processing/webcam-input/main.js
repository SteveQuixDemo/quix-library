var express = require('express');
var ejs = require('ejs');

const port = 80;

var app = express();

module.exports = app;

app.set('view engine', 'ejs');
app.use('/css', express.static('css'));

console.log("ENV --- ");
console.log(process.env);
console.log("ENV --- ");

app.get('/', (req, res) => {
    res.render("index", {
        env: process.env,
        topic_name: process.env["topic-raw"].substring( process.env.Quix__Workspace__Id.length )
    });
})



app.listen(port, () => console.log(`Server running at http://127.0.0.1:${port}`))
