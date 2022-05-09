


// send request to server to delete the contact
const deleteContact = (id) => {
    console.log(id)
    fetch('/delete-contact',{
        method:"DELETE",
        body : JSON.stringify({id})
    }).then((res)=>{
        console.log(res)
        window.location.href = "/";
    })
}
