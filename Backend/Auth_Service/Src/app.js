require("dotenv").config();
const express = require("express");
const authRoutes = require("./routes/authRoutes");

const app = express();

const PORT = process.env.PORT||5001;

app.use(express.json());

app.get("/api/health", (req, res) => {
  res.json({
    status: "OK",
    service: "Auth Service",
  });
});

app.use("/api/auth", authRoutes);

app.listen(PORT, () => {
  console.log(`Auth Service running on port ${PORT}`);
});