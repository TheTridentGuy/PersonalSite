function $(id){
    return document.getElementById(id)
}
var main_color = "--main-color"
var main_bg = "--main-bg"
$(main_color).addEventListener("change", () => {
    document.documentElement.style.setProperty(main_color, $(main_color).value)
    localStorage.setItem(main_color, $(main_color).value)
})
$(main_bg).addEventListener("change", () => {
    document.documentElement.style.setProperty(main_bg, $(main_bg).value)
    localStorage.setItem(main_bg, $(main_bg).value)
})
if(localStorage.getItem(main_color)){
    $(main_color).value = localStorage.getItem(main_color)
}
if(localStorage.getItem(main_bg)){
    $(main_bg).value = localStorage.getItem(main_bg)
}
document.querySelectorAll('[data-date]').forEach(element => {
    var date = new Date(element.dataset.date);
    var current = new Date();
    var diff = current.getFullYear() - date.getFullYear();
    var adjusted = (current.getMonth() > date.getMonth() || 
                           (current.getMonth() == date.getMonth() && 
                            current.getDate() >= date.getDate()))
                            ?diff:diff-1;
    element.innerText = adjusted;
});
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}
function toggle_preview(){
    var url = new URL(window.location.href);
    var params = new URLSearchParams(url.search);
    if(params.get("preview") == "true"){
        params.set("preview", "false")
        window.location.replace(url.origin+url.pathname)
    }else{
        params.set("preview", "true")
        url.search = params.toString();
        window.location.replace(url.origin+url.pathname+url.search)
    }
}
if($("jumpscare")){
fetch('https://api.nekosapi.com/v3/images/random?rating=safe&limit=1&tag=8')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const img = document.createElement('img');
        img.src = data.items[0].image_url;
        $("jumpscare").appendChild(img);
    })
    .catch(error => console.error('Error fetching JSON:', error));
}