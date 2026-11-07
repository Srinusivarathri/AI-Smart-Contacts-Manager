const pool=require("../config/db.js");

const createContact= async(name,phone,email)=>{
    const {rows}=await pool.query(
        "INSERT INTO contacts (name,phone,email) VALUES($1,$2,$3) RETURNING *",
        [name,phone,email || null]
    );
    return rows[0];
};

const getContacts=async()=>{
    const {rows}=await pool.query(
        "SELECT * FROM contacts",
    );
    return rows;
};
const getContactsById=async(id)=>{
    const {rows}=await pool.query(
        "SELECT * FROM contacts WHERE id=$1",
        [id]
    );
    return rows[0];
};

const updateContact=async(id,name,phone,email)=>{
    const {rows}=await pool.query(
        "UPDATE contacts SET name =$1,phone=$2,email=$3 WHERE ID=$4 RETURNING *",
        [name,phone,email,id]
     );
     return rows[0];
};
const deleteContact=async(id)=>{
    const {rows}=await pool.query(
        "DELETE FROM contacts WHERE id=$1 RETURNING *",
        [id]
    );
};
module.exports={createContact,getContacts,getContactsById,updateContact,deleteContact};