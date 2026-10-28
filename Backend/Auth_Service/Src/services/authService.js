const bcrypt = require("bcryptjs");
const pool = require("../config/db");
const jwt=require("jsonwebtoken")

const registerUser = async (email, password) => {
  const existingUser = await pool.query(
    "SELECT id FROM users WHERE email = $1",
    [email]
  );

  if (existingUser.rows.length > 0) {
    throw new Error("User already exists");
  }

  const passwordHash = await bcrypt.hash(password, 10);

  const result = await pool.query(
    `INSERT INTO users (email, password_hash)
     VALUES ($1, $2)
     RETURNING id, email, created_at`,
    [email, passwordHash]
  );

  return result.rows[0];
};

const loginUser=async(email,password)=>{
  const result=await pool.query(
    "SELECT id,email,password_hash FROM users where email=$1",
    [email]
  );
  if(result.rows.length==0){
    throw new Error("Invalid Credentials");
  }
  const user=result.rows[0];
  const isPasswordValid=await bycrypt.compare(
    password,
    user.password_hash
  );
  if(!isPasswordValid){
    throw new Error("Invalid Credentials");
  }
  const token=jwt.sign(
    {
      userId: user.id,
      email: user.email,
    },
    process.env.JWT_SECRET,
    {
      expiresIn: "1h",
    }
  )
  return {
    id:user.id,
    emai:user.email,
    token,
  };
}
module.exports={
  registerUser,
  loginUser,
}