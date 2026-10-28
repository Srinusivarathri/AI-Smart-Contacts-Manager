const express =require("express");
const{
    createContact,
    getContacts,
    getContactsById,
    updateContact,
    deleteContact 
 } =require("../controllers/contactController");
 
const router =express.Router();

router.post("/",createContact);
router.get("/",getContacts);
router.get("/:id",getContactsById);
router.put("/:id",updateContact)
router.delete("/:id",deleteContact);

module.exports=router;