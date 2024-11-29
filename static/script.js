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