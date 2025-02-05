/*
This script will run before the document loads:
*/
function $(id) {
  return document.getElementById(id);
}
var main_color = "--main-color";
var main_bg = "--main-bg";
if (localStorage.getItem(main_color)) {
  document.documentElement.style.setProperty(
    main_color,
    localStorage.getItem(main_color)
  );
}
if (localStorage.getItem(main_bg)) {
  document.documentElement.style.setProperty(
    main_bg,
    localStorage.getItem(main_bg)
  );
}
