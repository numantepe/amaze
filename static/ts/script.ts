{
let webURL : string = "http://127.0.0.1:5000";
let search_product = document.querySelector("#search-product") as HTMLInputElement;
let min_price = document.querySelector("#min-price") as HTMLInputElement;
let max_price = document.querySelector("#min-price") as HTMLInputElement;
let min_num_of_stars = document.querySelector("#min-num-of-stars") as HTMLInputElement;
let max_num_of_stars = document.querySelector("#max-num-of-stars") as HTMLInputElement;
let min_num_of_ratings = document.querySelector("#min-num-of-ratings") as HTMLInputElement;
let max_num_of_ratings = document.querySelector("#max-num-of-ratings") as HTMLInputElement;
let max_num_of_products = document.querySelector("#max-num-of-products") as HTMLInputElement;
let chosen_op : string = "op1";
let chosen_country: string = "ca";

let send_message_to_server_list = document.querySelectorAll(".send-message-to-server");   
for(let i = 0; i < send_message_to_server_list.length; i++)
{
    let send_message_to_server = send_message_to_server_list[i] as HTMLElement; 

    send_message_to_server.addEventListener("click", function (e) {
        e.preventDefault();

        if(e.target instanceof Element){
            if(e.target.classList.contains("option-btn")){
                let options = document.querySelectorAll(".option-btn");
                for(let i = 0; i < options.length; i++)
                {
                    (options[i]).classList.remove("chosen-option");
                }
                e.target.classList.add("chosen-option");
                chosen_op = e.target.id;
            }

            if(e.target.classList.contains("img-country")){
                let countries = document.querySelectorAll(".div-country");
                for(let i = 0; i < countries.length; i++)
                {
                    (countries[i]).classList.remove("chosen-country");
                }
                e.target.parentElement.classList.add("chosen-country");
                chosen_country = e.target.id;

                let desc = document.querySelector("#amazon");
                if(chosen_country === "ca"){
                    desc.textContent = "Amazon.ca";
                }
                else{
                    desc.textContent = "Amazon.com";
                }
            }
        }

        let xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200){
                console.log("Response Type " + this.responseType);
                console.log("Response Text " + this.responseText);
                }
        };
        
        const apiURL = `${webURL}/search-product`;
        xhttp.open("POST", apiURL, true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("search_product="+search_product.value.trim()+"&min_price="+min_price.value.trim()
                    +"&max_price="+max_price.value.trim()
                    +"&min_num_of_stars="+min_num_of_stars.value.trim()+"&max_num_of_stars="+max_num_of_stars.value.trim()
                    +"&min_num_of_ratings="+min_num_of_ratings.value.trim()
                    +"&max_num_of_ratings="+max_num_of_ratings.value.trim()
                    +"&max_num_of_products="+max_num_of_products.value.trim()
                    +"&chosen_op="+chosen_op+"&chosen_country="+chosen_country);
    });
}
}
