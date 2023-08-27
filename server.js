require('./config/mongo') // Requires the mongodb file

const express = require("express") //requires express.js
const app=express() //Launches express.js

const port = process.env.PORT || 3000

const UserRouter = require('./api/User')

// For accepting post form data (JSON) Don't forget to require the body-parser THIS WAS THE BIG ERROR WE NEED TO PARSE TO GET DATA
const bodyParser = require("express").json; 
app.use(bodyParser()); // Use body-parser middleware THIS WAS THE BIG ERROR WE NEED TO PARSE TO GET DATA

const path=require("path")
const nodemailer = require('nodemailer');

app.use("/user", UserRouter)

app.listen(port ,() => { //Asks express.js to listen to port #3000 (TCP port for running web applications), 2nd parameter is the function
    console.log("Port connected");  // Affirms port connection

})