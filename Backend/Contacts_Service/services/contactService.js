const pool=require("../config/db.js");

const createContact= async(name,phone,email)=>{
    const {rows}=await pool.query(
        "INSERT INTO contacts (name,phone,email) VALUES($1,$2,$3) RETURNING *",
        [name,phone,email || null]
    );
    return rows[0];
};

const getContacts=async(filters={})=>{
    const {name,relation,address}=filters;
    const conditions=[];
    const values=[];

    if(name){
        values.push(`%${name}%`);
        conditions.push(`name ILIKE $${values.length}`);
    }
    if(relation){
        values.push(relation);
        conditions.push(`Lower(relation)=Lower($${values.length})`);
    }
    if(address){
        values.push(`%${address}%`);
        conditions.push(`address ILIKE $${values.length}`);
    }
    let sql="SELECT * FROM contacts";
    if(conditions.length>0){
        sql+=" WHERE " + conditions.join(" AND ");
    }
    const {rows}=await pool.query(sql,values);
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