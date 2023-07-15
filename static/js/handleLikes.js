async function request(data) {
   return await fetch("/like", {
      method: "POST",
      headers: {
         "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
   });
}
async function requestHandler(opt, user_id, table, post_id) {
   await request({ opt, user_id, table, post_id })
      .then((res) => {
         if (res.ok) window.location.href = "/home";
         else throw new Error("Error en la peticion");
      })
      .catch((err) => {
         throw new Error(`Error: ${err}`);
      });
}

async function handleLikeClick(link) {
   let opt = "like";
   
   const post_id = link.getAttribute("data-post-id");
   const user_id = link.getAttribute("data-user");
   const button_type = link.getAttribute("data-type-button");
   const table = link.getAttribute("data-table");
   

   if (button_type === "like") {

      link.innerHTML =
         '<img src="https://res.cloudinary.com/dm8e8z3bo/image/upload/f_auto,q_auto/v1689349940/app_citas/icons/dislike.svg" alt="dislike button">';
      link.setAttribute("data-type-button", "dislike");
      await requestHandler(opt, user_id, table, post_id);

   } else if (button_type === "dislike") {

      let opt = "dislike";

      link.innerHTML =
         '<img src="https://res.cloudinary.com/dm8e8z3bo/image/upload/f_auto,q_auto/v1689349996/app_citas/icons/like.svg" alt="like button">';
      link.setAttribute("data-type-button", "like");
      await requestHandler(opt, user_id, table, post_id);
   }
}
