const express = require("express");
const { register } = require("../controllers_temp/authController");

const router = express.Router();

router.post("/register", register);
router.get("/login",login);

module.exports = router;