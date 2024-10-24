const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const UsersSchema = new Schema({
    name: {
        type: String,
        required: true
    },
    cin: {
        type: Number,   // Numeric type
        required: true, // Field is required
        validate: {
          validator: Number.isInteger,  // Ensures the value is an integer
          message: '{VALUE} is not an integer value'
        },
        unique: true 
      },
    role:{
        type:String,
        required:true
    },
    email: {
        type: String,
        required: true,
        unique: true  // Automatically creates a unique index for 'email'
    },
    password: {
        type: String,
        required: true
    },
    entries: {
        type: Number,
        default: 0
    },
    date: {
        type: Date,
        default: Date.now  // Use Date.now without parentheses
    },
    image: {
        data: Buffer,         // Store the image data as a buffer (binary data)
        contentType: String   // Store the MIME type of the image (e.g., 'image/png', 'image/jpeg')
    }
});

// Mongoose will automatically create indexes, so no need to call createIndexes()
const User = mongoose.model('FaceDetection', UsersSchema);

module.exports = User;
