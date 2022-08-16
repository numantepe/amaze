{
interface Product {
    desc: string,
    url: string,
    image: string,
    price: number,
    stars: number,
    ratings: number
    max_ratings_min_price: number,
    max_stars_min_price: number,
    max_ratings_max_stars: number,
    max_ratings_max_stars_min_price: number
}

let webURL : string = "http://127.0.0.1:5000";
let search_product = document.querySelector("#search-product") as HTMLInputElement;
let min_price = document.querySelector("#min-price") as HTMLInputElement;
let max_price = document.querySelector("#max-price") as HTMLInputElement;
let min_num_of_stars = document.querySelector("#min-num-of-stars") as HTMLInputElement;
let max_num_of_stars = document.querySelector("#max-num-of-stars") as HTMLInputElement;
let min_num_of_ratings = document.querySelector("#min-num-of-ratings") as HTMLInputElement;
let max_num_of_ratings = document.querySelector("#max-num-of-ratings") as HTMLInputElement;
let max_num_of_products = document.querySelector("#max-num-of-products") as HTMLInputElement;
let chosen_op : string = "op1";
let chosen_country: string = "ca";

let product_list = document.querySelector(".product-list") as HTMLElement;

let products_json: Product[] = [];

function set_up_product_list(products : Product[]) : void {
    product_list.textContent = "";

    let minpriceval = min_price.value.trim();
    if(minpriceval === ""){
        minpriceval = "-999999";
    }
    let minpricefloat = parseFloat(minpriceval);

    let maxpriceval = max_price.value.trim();
    if(maxpriceval === ""){
        maxpriceval = "999999";
    }
    let maxpricefloat = parseFloat(maxpriceval);

    let minstarsval = min_num_of_stars.value.trim(); 
    if(minstarsval === ""){
        minstarsval = "-999999";
    }
    let minstarsfloat = parseFloat(minstarsval);

    let maxstarsval = max_num_of_stars.value.trim(); 
    if(maxstarsval === ""){
        maxstarsval = "999999";
    }
    let maxstarsfloat = parseFloat(maxstarsval);

    let minratingsval = min_num_of_ratings.value.trim(); 
    if(minratingsval === ""){
        minratingsval = "-999999";
    }
    let minratingsint = parseInt(minratingsval);

    let maxratingsval = max_num_of_ratings.value.trim(); 
    if(maxratingsval === ""){
        maxratingsval = "999999";
    }
    let maxratingsint = parseInt(maxratingsval);

    let maxproductsval = max_num_of_products.value.trim(); 
    if(maxproductsval === ""){
        maxproductsval = products.length.toString();
    }
    let maxproductsint = parseInt(maxproductsval);

    for (let i = 0; i < maxproductsint; i++)
    {
        let product = products[i];

        if((minpricefloat <= product.price && product.price <= maxpricefloat) && 
           (minstarsfloat <= product.stars && product.stars <= maxstarsfloat) && 
           (minratingsint <= product.ratings && product.ratings <= maxratingsint)){
                product_list.insertAdjacentHTML("beforeend", `<li class="product">
                    <img src="${product.image}">
                    <a href="${product.url}" target="_blank">
                        ${product.desc}
                    </a>
                    <span class="price">$${product.price}</span>
                    <span class="num-of-stars">${product.stars} stars</span>
                    <span class="num-of-ratings">${product.ratings} ratings</span>
                </li>`);
        }
   }
}

let option_buttons = document.querySelectorAll(".option-btn");
for(let i = 0; i < option_buttons.length; i++)
{
    let option_button = option_buttons[i] as HTMLElement; 
    option_button.addEventListener("click", function(e) {
        e.preventDefault();

        if(e.target instanceof Element){
            let options = document.querySelectorAll(".option-btn");
            for(let i = 0; i < options.length; i++)
            {
                (options[i]).classList.remove("chosen-option");
            }
            e.target.classList.add("chosen-option");
            chosen_op = e.target.id;

            set_up_product_list(products_json);
        }
    });
}

document.querySelector("#form-submit").addEventListener("click", function(e) {
    e.preventDefault();

    set_up_product_list(products_json);
});

let send_message_to_server_list = document.querySelectorAll(".send-message-to-server");   
for(let i = 0; i < send_message_to_server_list.length; i++)
{
    let send_message_to_server = send_message_to_server_list[i] as HTMLElement; 

    send_message_to_server.addEventListener("click", function (e) {
        e.preventDefault();
        
        if(e.target instanceof Element){
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
                product_list.textContent = "";
            }
        }

        if(search_product.value.trim() !== "")
            {
            let xhttp = new XMLHttpRequest();

            xhttp.onreadystatechange = function() {
                if (this.readyState === 4 && this.status === 200){
                    console.log("Response Type " + this.responseType);
                    console.log("Response Text " + this.responseText);

                    let response = this.responseText;

                    let convertedResponse = JSON.parse(response);
                    products_json = convertedResponse;

                    set_up_product_list(products_json);
                    document.querySelector(".main-middle .msg").textContent = "";
                    }
            };
            
            const apiURL = `${webURL}/search-product`;
            xhttp.open("POST", apiURL, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("search_product="+search_product.value.trim()+"&chosen_country="+chosen_country);
            document.querySelector(".main-middle .msg").textContent = "Please wait a little while until the results show up.";
        }
    });
}
}
