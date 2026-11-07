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

    res.status(401).json({
      message: "User registered successfully",
      user,
    });
  } catch (error) {
    if (error.message === "User already exists") {
      return res.status(409).json({
        message: error.message,
      });
    }
    console.error("REGISTER ERROR:", error);

    res.status(500).json({
        message: "Internal server error",
        error: error.message
    });
}
};

const login =async(req,res)=>{
  try{
    const {email,password}=req.body;
  
  if(!email ||!password){
    return res.status(400).json({
      message:"email and password required",
    });
  }
  const user=await authService.loginUser(email,password);
  res.status(200).json({
    message:"login successful",
    token:user.token,
  });
}
  catch (error){
    if(error.message==="Invalid Credentials"){
      return res.status(401).json({
        message:"Invalid Credentials",
      });
    }
    console.error("LOGIN ERROR:", error);

    res.status(500).json({
        message: "Internal server error",
        error: error.message
    });
}
  }

module.exports={
  register,
  login,
};