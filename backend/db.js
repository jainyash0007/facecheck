const ENV=require('dotenv').config()
const mongoose = require('mongoose');
const mongoURI = process.env.MONGO_URI;


const connectToMongo = async () => {
  try {
    await mongoose.connect(mongoURI);
    console.log('Connected to MongoDB');
  } catch (error) {
    console.error('Failed to connect to MongoDB Bro:', error.message);
  }
};

module.exports = connectToMongo;
