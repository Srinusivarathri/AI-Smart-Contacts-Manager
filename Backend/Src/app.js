const express = require("express");
const authRoutes = require("./routes/authRoutes");

const app = express();

const PORT = 5000;

app.use(express.json());

app.get("/api/health", (req, res) => {
  res.json({
    status: "OK",
    service: "AI Smart Contacts Manager",
  });
});

app.use("/api/auth", authRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});