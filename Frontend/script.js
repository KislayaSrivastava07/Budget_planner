const API = "http://127.0.0.1:8000";

function addTransaction(){

const title = document.getElementById("title").value;
const amount = document.getElementById("amount").value;
const category = document.getElementById("category").value;
const type = document.getElementById("type").value;

fetch(`${API}/add-transaction`,{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
title:title,
amount:amount,
category:category,
type:type
})

})
.then(res=>res.json())
.then(data=>{
alert("Transaction Added");
loadTransactions();
})

}


function loadTransactions(){

fetch(`${API}/transactions`)
.then(res=>res.json())
.then(data=>{

const table=document.querySelector("#transactionTable tbody");

table.innerHTML="";

data.forEach(t=>{

const row=`
<tr>
<td>${t.id}</td>
<td>${t.title}</td>
<td>${t.amount}</td>
<td>${t.category}</td>
<td>${t.type}</td>
</tr>
`;

table.innerHTML+=row;

});

});

}