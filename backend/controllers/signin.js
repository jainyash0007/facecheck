const handleSignin = async (req, res, User, bcrypt) => {
  const { email, password } = req.body;
  if (!password || !email) {
    return res.status(400).json('incorrect form submission');
  }

  try {
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json('wrong credentials');
    }

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      return res.status(400).json('wrong credentials');
    }

    res.json(user);
  } catch (error) {
    console.error(error);
    res.status(500).json('Internal Server Error');
  }
};

module.exports = {
  handleSignin: handleSignin,
};
