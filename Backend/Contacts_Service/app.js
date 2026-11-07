require("dotenv").config();
const express=require("express");
const contactRoutes=require("./routes/contactRoutes");
const app =express();
const PORT=process.env.PORT||5002;
app.use(express.json());
app.use("/api/contacts",contactRoutes);
app.listen(PORT,()=>{
    console.log(`Contacts Service is running on${PORT}`);
})