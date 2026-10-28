const contactService=require("../services/contactService");
const createContact=async(req,res)=>{
    try{
        const {name,phone,email}=req.body;
        if(!name || !phone){
            return res.status(400).json({
                message:"name and phone required",
            });
        }
        const user=await contactService.createContact(name,phone,email);
        return res.status(201).json(user)   
}
catch(err){
    return res.status(500).json({message:err.message});
    }
};

const getContacts=async(req,res)=>{
    try{
        const contacts=await contactService.getContacts();
        return res.json(contacts);
    }
    catch(err){
        return res.status(500).json({message:err.message});
        }
    };

const getContactsById=async(req,res)=>{
    try{
        const{id}=req.params;
        const contact=await contactService.getContactsById(id);
        if(!contact){
            return res.status(404).json({message:"contact not found"});
        }
        return res.json(contact);
    }
    catch(err){
        return res.status(500).json({message:err.message});
    }
}; 

const updateContact=async(req,res)=>{
   try{
    const {id}=req.params;
    const {name,phone,email}=req.body;
    const contact=await contactService.updateContact(id,name,phone,email);
    if(!contact){
        return res.status(404).json({message:"contact not found"});
    }
    return res.json(contact);
   }
   catch(err){
    return res.status(500).json({message:err.message});
   }
};

const deleteContact=async(req,res)=>{
    try{
        const {id}=req.params;
        const contact=await contactService.deleteContact(id);
        if(!contact){
            return res.status(404).json({message:"contact not found"});
        }
        return res.status(200).json({message:"deleted successfully"});
    }
    catch(err){
        return res.status(500).json({message:err.message});
    }
};

module.exports={createContact,getContacts,getContactsById,updateContact,deleteContact};
