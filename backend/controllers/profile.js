const handleProfile = async (req, res, User) => {
  const { id } = req.params;
  try {
    const user = await User.findById(id);
    if (!user) {
      return res.status(400).json('user not found');
    }

    res.json(user);
  } catch (error) {
    console.error(error);
    res.status(500).json('Internal Server Error');
  }
};

module.exports = {
  handleProfile: handleProfile,
};
