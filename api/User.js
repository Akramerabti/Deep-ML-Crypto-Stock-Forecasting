const express = require('express')
const router = express.Router();

//mongodb user model
const user = require("./../models/User");
const User = require('./../models/User');

//Password handler
const bcrypt = require("bcrypt")

//Signup

router.post('/signup', (req, res) =>{ //Posts an action called signup in the whole system file while asking for a request and response (to work with mongodb, we write async)

    let {name, email,password,dateOfBirth} = req.body;
    name = name.trim();
    email = email.trim();
    password = password.trim();
    dateOfBirth = dateOfBirth.trim();

    if (name == "" || email == "" || password == "" || dateOfBirth == "") {
         res.json({
            status:"Failed",
            message: "Empty input fields"
         });
    }
    else if (!/^[a-zA-Z ]*$/.test(name)) { //else if the name is not a regular expression, we update the status
        res.json({
            status: "Failed",
            message: "Invalid name"

        })
    }
    else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) { //else if the email is not of format masdosdao@okmasdok.koasd , we update status
        res.json({
            status: "Failed",
            message: "Invalid email"

        })
    }

    else if (!new Date(dateOfBirth).getTime()) { //else if the date is invalid ( the exclamation mark says we do not get a time from the date)
        res.json({
            status: "Failed",
            message: "Invalid date of birth"

        })
    }

    else if (/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/.test(password) ) { //else if the password is too short
        res.json({
            status: "Failed",
            message: "Password must contain minimum eight characters, at least one letter, one number and one special character "

        })
    }

else {
    User.find({email}).then(result => {
        if (result.length) {
            // A user exists since a length value is returned
            res.json({
                status: "Failed",
                message: "User with the provided email already exists"
            })
        } 
        else {
            //Try create new user

            //password handling: Hashing password
            const saltRounds = 10;
            bcrypt.hash(password, saltRounds).then(hashedPassword => {
                const newUser = new User({
                    name,
                    email,
                    password: hashedPassword,
                    dateOfBirth
                })

                newUser.save().then(result => {
                    res.json({
                        status: "Success",
                        message: "Signup Successful"
                })
            })
            
            .catch(err => {
                res.json({
                    status: "Failed",
                    message: "Error while saving user password"
                })
            })
        })
            .catch(err => {
                res.json({
                    status: "Failed",
                message: "An error while hashing password"
                })
            })

        }
    }).catch(err =>{
        console.log(err)
        res.json({
            status: "Failed",
            message: "Error occured while verification for existing user"
        })
    })
}

});


//Login
router.post('/login', (req, res) => {

    let {name, email, password} = req.body;
    name = name.trim();
    email = email.trim();
    password = password.trim();

    if (name == "" && email == "" || password == "" ) {
        res.json({
           status:"Failed",
           message: "Empty credentials"
        });
        
   }
   else if (User.find({name})) {
    if (data) {
        const hashedPassword = data[0].password
        bcrypt.compare(password, hashedPassword).then(result => {
            if(result) {
                res.json({
                    status:"Success",
                    message: "Sign in successful",
                    data: data
                 });
            } else {
                res.json({
                    status:"Failed",
                    message: "Invalid Password",
                    })
                }
            })
.catch(err => {
    res.json({
        status:"Failed",
        message: "Error occured when comparing passwords",
        })    
    })
}
else {
res.json({
    status:"Failed",
    message: "Invalid credentials",
    })
}
}

   else {
    User.find({email}).then(data => { //if theres an email, we compare the password output to the password in database
        if (data) {
            const hashedPassword = data[0].password
            bcrypt.compare(password, hashedPassword).then(result => {
                if(result) {
                    res.json({
                        status:"Success",
                        message: "Sign in successful",
                        data: data
                     });
                } else {
                    res.json({
                        status:"Failed",
                        message: "Invalid Password",
                        })
                    }
                })
    .catch(err => {
        res.json({
            status:"Failed",
            message: "Error occured when comparing passwords",
            })    
        })
    }
    else {
    res.json({
        status:"Failed",
        message: "Invalid credentials",
        })
    }
})
.catch(err => {
    res.json({
    status:"Failed",
    message: "Error occured when checking user",
    
    })
})
}
})


module.exports= router