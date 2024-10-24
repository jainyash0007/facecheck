const connectToMongo = require('./db.js');
const ENV = require('dotenv').config();
const bodyParser = require('body-parser');
const express = require('express');
const bcrypt = require('bcrypt');
const port = 5000;
const User = require('./models/register');

const cors = require('cors');
const register = require('./controllers/register');
const signin = require('./controllers/signin');
const profile = require('./controllers/profile');
const image = require('./controllers/image');
const path = require('path');

initializeApp();
const app = express();

// Middleware
app.use(cors());
app.use(express.static(path.resolve(__dirname, 'build')));
app.use(bodyParser.json());

// Routes
app.post('/signin', (req, res) => signin.handleSignin(req, res, User, bcrypt));
app.post('/register', (req, res) => register.handleRegister(req, res, User, bcrypt));
app.get('/profile/:id', (req, res) => profile.handleProfile(req, res,User));

// Route for image upload (both checking if the image exists and adding new images)
app.post('/upload-image', (req, res) => image.handleImage(req, res));
app.get('/get-image/:id', (req, res) => image.getImage(req, res));
app.post('/check-cin-email', (req, res) => register.handleCINAndEmailCheck(req, res,User));
// Function to connect to MongoDB
async function initializeApp() {
  try {
    await connectToMongo();
    console.log('Connected to MongoDB Successfully');
  } catch (error) {
    console.error('Failed to connect to MongoDB:', error.message);
  }
}

// Start the server
app.listen(port, () => {
  console.log(`SmartBrain backend listening at http://localhost:${port}`);
});
