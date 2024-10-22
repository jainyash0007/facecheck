const saltRounds = 10;

const handleRegister = async (req, res, User, bcrypt) => {
  const { email, password, name } = req.body;
  if (!name || !password || !email) {
    return res.status(400).json('incorrect form submission');
  }

  try {
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    const newUser = new User({
      name,
      email,
      password: hashedPassword,
      entries: 0,
    });
    const savedUser = await newUser.save();
    res.json(savedUser);
  } catch (error) {
    console.log(error);
    res.status(400).json('unable to register');
  }
};

module.exports = {
  handleRegister: handleRegister,
};
