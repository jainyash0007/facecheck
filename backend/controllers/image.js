const multer = require('multer');
const User = require('../models/register'); // Your User model

// Set up Multer to store images in memory as a buffer
const storage = multer.memoryStorage();
const upload = multer({ storage });

const handleImage = async (req, res) => {
  upload.single('image')(req, res, async (err) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to upload image', details: err });
    }

    try {
      const userId = req.body.userId;  // Ensure this is being received
      const user = await User.findById(userId);  // Find the user in your database

      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      if (!req.file) {
        return res.status(400).json({ error: 'No image file uploaded' });
      }

      // Save the image to the user's document
      user.image = {
        data: req.file.buffer,           // Store binary data (Buffer)
        contentType: req.file.mimetype   // Store MIME type (e.g., 'image/png')
      };

      await user.save();  // Save the updated user with the image

      res.json({ message: 'Image uploaded successfully' });
    } catch (error) {
      res.status(500).json({ error: 'Failed to upload and save image', details: error });
    }
  });
};

const getImage = async (req, res) => {
  try {
   
    const userId = req.params.id; // Get the user ID from the URL params
    const user = await User.findById(userId); // Find the user by ID

    if (!user || !user.image) {
      return res.status(404).json({ error: 'Image not found' });
    }

    // Set the content type and send the image data as binary
    res.set('Content-Type', user.image.contentType);
    res.send(user.image.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve image', details: error });
  }
};


module.exports = {
  handleImage, getImage
};
