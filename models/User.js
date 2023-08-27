const mongoose = require('mongoose')

const UserSchema =new mongoose.Schema({ // Creates a User Schema for our database
    name: String,
    email: String,
    password: String,
    dateOfBirth: Date

})

const User = mongoose.model ("User", UserSchema ) //Creation of collection with name user inside the database following the UserSchema

module.exports = User //To get the user in the files