const saltRounds = 10;

const handleRegister = async (req, res, User, bcrypt) => {
  const { email, password, name, cin, role } = req.body;
  if (!name || !password || !email || !cin || !role) {
    return res.status(400).json('incorrect form submission');
  }

  try {
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    const newUser = new User({
      name,
      cin,
      role,
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


// Check if CIN exists
const handleCINAndEmailCheck = async (req, res,User) => {
  const { cin, email } = req.body;

  try {
    // Check for existing CIN
    const existingCIN = await User.findOne({ cin });


    
    if (existingCIN) {
      return res.status(400).json({ message: 'CIN already exists' });
    }

    // Check for existing email
    const existingEmail = await User.findOne({ email });
    if (existingEmail) {
      return res.status(400).json({ message: 'Email already exists' });
    }

    return res.status(200).json({ message: 'CIN and Email are available' });
  } catch (error) {
    return res.status(500).json({ message: 'Error checking CIN and Email', error });
  }
};

module.exports = {
  handleRegister: handleRegister,
  handleCINAndEmailCheck
};
