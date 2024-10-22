const connectToMongo = require('./db.js');
const ENV=require('dotenv').config()
const bodyParser = require('body-parser');
const express = require('express');
const bcrypt = require('bcrypt');
const port = 5000
const User = require('./models/register');

const cors = require('cors');
const register = require('./controllers/register')
const signin = require('./controllers/signin')
const profile = require('./controllers/profile')
const image = require('./controllers/image')
const path = require('path');

initializeApp();
const app = express();
app.use(cors())
app.use(express.static(path.resolve(__dirname, 'build')));

app.use(bodyParser.json())
app.post('/signin', (req, res) => {signin.handleSignin(req,res,User,bcrypt)})
app.post('/register', (req, res) => {register.handleRegister(req,res,User,bcrypt)})
app.get('/profile/:id', (req, res) => { profile.handleProfile(req, res, User)})
app.put('/image', (req, res) => {image.handleImage(req,res,User)})
async function initializeApp() {
    try {
      await connectToMongo();
      console.log('Connected to MongoDB Successfully');
    } catch (error) {
      console.error('Failed to connect to MongoDB:', error.message);
    }
  }
app.listen(port, () => {
    console.log(`SmartBrain backend listening at http://localhost:${port}`)
})