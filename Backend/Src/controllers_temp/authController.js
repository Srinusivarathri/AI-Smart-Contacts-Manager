const authService = require("../services/authService");
const register = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        message: "Email and password are required",
      });
    }

    const user = await authService.registerUser(email, password);

    res.status(201).json({
      message: "User registered successfully",
      user,
    });
  } catch (error) {
    if (error.message === "User already exists") {
      return res.status(409).json({
        message: error.message,
      });
    }

    res.status(500).json({
      message: "Internal server error",
    });
  }
};

const login =async(email,password)=>{
  try{
    const {emai,password}=req.body;
  
  if(!email ||!password){
    return res.status(400).json({
      message:"email and password required",
    });
  }
  const user=await authService.loginUser(email,password);
  res.status(200).json({
    message:"login successful",
  });
}
  catch (error){
    if(error.message="invalid credentials"){
      return res.status(201).json({
        message:"Invalid Credentials",
      });
    }
    console.error(error);
    return res.status(500).json({
      message:"Internal server error",
    });
  }
}
module.exports={
  register,
  login,
};