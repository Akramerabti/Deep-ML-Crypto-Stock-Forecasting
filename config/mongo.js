const mongoose=require("mongoose")

mongoose.connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  }) //Used to connect the node of our local hosting network to mongodb database with the name after the local host setup
.then(()=>{
    console.log("mongoose connected"); //Prints connection if it works
})
.catch(()=>{
    console.log("failed to connect to database"); //Prints connection if it didn't work
});
