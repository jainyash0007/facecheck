const handleImage = async (req, res, User) => {
  const { id } = req.body;
  try {
    const user = await User.findByIdAndUpdate(
      id,
      { $inc: { entries: 1 } },
      { new: true }
    );
    if (!user) {
      return res.status(400).json('unable to get entries');
    }

    res.json(user.entries);
  } catch (error) {
    console.log(error);
    res.status(500).json('Internal Server Error');
  }
};

module.exports = {
  handleImage: handleImage,
};
