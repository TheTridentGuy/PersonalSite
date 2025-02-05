const aud = [
  {
    id: 1,
    title: "Double Furry Power",
    artist: "Cyberhound",
    cover: "https://i1.sndcdn.com/artworks-000257648129-ev94t0-t200x200.jpg",
    mp3: "/static/music/357185573.mp3",
  },
  {
    id: 2,
    title: "Diamond Heart",
    artist: "Alan Walker",
    cover: "https://i1.sndcdn.com/artworks-S3NAnj8CI0lS-0-t200x200.jpg",
    mp3: "/static/music/394021557.mp3",
  },
  {
    id: 3,
    title: "Ritual",
    artist: "Alan Walker",
    cover: "https://i1.sndcdn.com/artworks-IdTIuye4Tree-0-t200x200.jpg",
    mp3: "/static/music/394021558.mp3",
  },
  {
    id: 4,
    title: "Avalon",
    artist: "Alan Walker",
    cover:
      "https://i1.sndcdn.com/artworks-mTVQWykswT2C91OM-M0fFSw-t200x200.jpg",
    mp3: "/static/music/394021159.mp3",
  },
  {
    id: 5,
    title: "CYBERNETIC HEART",
    artist: "ivycomb & Stephanafro",
    cover:
      "https://i1.sndcdn.com/artworks-74VTfkNK1s1sqWM5-7htYFg-t200x200.jpg",
    mp3: "/static/music/394021160.mp3",
  },
];

function snd(id) {
  return aud.find((song) => song.id === id);
}

function info(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

function cycle() {
  const audio = document.getElementById("audio");
  const play = document.querySelector("button svg");

  if (audio.paused) {
    audio.play();
    play.innerHTML = `
      <title>Pause</title>
      <path d="M1 12C1 5.925 5.925 1 12 1s11 4.925 11 11-4.925 11-11 11S1 18.075 1 12zm7.5-5a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h2a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-2zm5 0a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h2a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-2z"></path>
    `;
  } else {
    audio.pause();
    play.innerHTML = `
      <title>Play</title>
      <path d="M1 12C1 5.925 5.925 1 12 1s11 4.925 11 11-4.925 11-11 11S1 18.075 1 12zm8.75-4.567a.5.5 0 0 0-.75.433v8.268a.5.5 0 0 0 .75.433l7.161-4.134a.5.5 0 0 0 0-.866L9.75 7.433z"></path>
    `;
  }
}

function end() {
  const play = document.querySelector("button svg");
  play.innerHTML = `
    <title>Play</title>
    <path d="M1 12C1 5.925 5.925 1 12 1s11 4.925 11 11-4.925 11-11 11S1 18.075 1 12zm8.75-4.567a.5.5 0 0 0-.75.433v8.268a.5.5 0 0 0 .75.433l7.161-4.134a.5.5 0 0 0 0-.866L9.75 7.433z"></path>
  `;
}

function theme() {
  const mainColor = localStorage.getItem("--main-color");
  const mainBg = localStorage.getItem("--main-bg");

  if (mainColor) {
    document.documentElement.style.setProperty("--main-color", mainColor);
  }
  if (mainBg) {
    document.documentElement.style.setProperty("--main-bg", mainBg);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const songId = parseInt(info("id"), 10);
  const song = snd(songId);

  if (song) {
    document.getElementById("cover").src = song.cover;
    document.getElementById("title").textContent = song.title;
    document.getElementById("artist").textContent = song.artist;
    document.getElementById("audio").src = song.mp3;
  }

  const play = document.querySelector("button");
  play.addEventListener("click", cycle);

  const audio = document.getElementById("audio");
  audio.addEventListener("ended", end);

  // detect theme change
  window.addEventListener("storage", (event) => {
    if (event.key === "--main-color" || event.key === "--main-bg") {
      theme();
    }
  });
});

// preload.js
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
