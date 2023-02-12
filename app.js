require('dotenv').config();
const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const mongoose = require('mongoose');
const session = require('express-session')
const passport = require("passport");
const passportLocalMongoose = require("passport-local-mongoose");
const GoogleStrategy = require('passport-google-oauth20').Strategy;
var findOrCreate = require('mongoose-findorcreate')
const path = require("path");

const https = require("https")
const http = require("http")

console.log(process.env.CLIENT_ID);
console.log(process.env.CLIENT_SECRETS);

const app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(express.static("public"));

app.use(session({
    secret: "Our little secret",
    resave: false,
    saveUninitialized: false
}))
app.use(passport.initialize());
app.use(passport.session());

mongoose.set("strictQuery", false)
mongoose.connect("mongodb://0.0.0.0:27017/cropusers", function (err) {
    if (err) {
        console.log("Some error occured in the connecting to the database!");
    } else {
        console.log("Connected to the database Successfully");
    }
})

const UserSchema = new mongoose.Schema({
    username: String,
    password: String,
    googleId: String,
    secret: String
});

UserSchema.plugin(passportLocalMongoose);
UserSchema.plugin(findOrCreate);
const User = new mongoose.model("Users", UserSchema);
passport.use(User.createStrategy());

passport.serializeUser(function (user, done) {
    done(null, user);
});

passport.deserializeUser(function (user, done) {
    done(null, user);
});

passport.use(new GoogleStrategy({
    clientID: process.env.CLIENT_ID,
    clientSecret: process.env.CLIENT_SECRETS,
    callbackURL: "http://localhost:3000/auth/google/crops",
    scope:['profile']
  },
  function(accessToken, refreshToken, profile, cb) {
    console.log(profile);
    User.findOrCreate({ googleId: profile.id }, function (err, user) {
      return cb(err, user);
    });
  }
));

app.post("/auth/google",
  passport.authenticate('google', { scope: ["profile"] })
);

app.get("/auth/google/crops",
  passport.authenticate('google', { failureRedirect: "/login" }),
  function(req, res) {
    res.redirect("/crop");
  });

app.get("/crop",function(req,res){
    if (req.isAuthenticated()){
        res.render("crop");
      } else {
        res.send("Stay there bitch !!")
      }
})
app.post("/crop",function(req,res){
  res.redirect("/crop");
})

app.get("/",function(req,res,err){
  var strin = "";
  var linki = "";
    if(req.isAuthenticated()){
        strin = "Service";
        linki = "/crop";
    }
    else{
        strin = "Download";
        linki = "/auth/google";
    }
    res.render("index",{buttonsornot:{
      name:strin,
      link:linki
    }});
})

app.post("/model",function(req,res){
    console.log(req.body)
    console.log(req.body.state);
    res.sendFile('views/please.html', {root: __dirname })
    // so untill the process will be there we will render the please wait file 
    const url = "http://127.0.0.1:5000/?state="+ req.body.state +"&district=" + req.body.district + "&n=" + req.body.n.toString() + "&p=" + req.body.p.toString() + "&k=" + req.body.k.toString() + "&ph=" + req.body.ph.toString();
    console.log(url);
    http.get(url,function(response){
      response.on("data",function(data){
        console.log(data);
      })
    })
});

app.listen(3000, function() {
    console.log("Server started on port 3000");
  });