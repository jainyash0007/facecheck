const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const UsersSchema = new Schema({
    name: {
        type: String,
        required: true
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
    }
});

// Mongoose will automatically create indexes, so no need to call createIndexes()
const User = mongoose.model('FaceDetection', UsersSchema);

module.exports = User;
