const wrapper = document.querySelector(".wrapper"),
      musicImg = wrapper.querySelector(".img-area img"),
      musicName = wrapper.querySelector(".song-details .name"),
      musicArtist = wrapper.querySelector(".song-details .artist"),
      playPauseBtn = wrapper.querySelector(".play-pause"),
      prevBtn = wrapper.querySelector("#prev"),
      nextBtn = wrapper.querySelector("#next"),
      mainAudio = wrapper.querySelector("#main-audio"),
      progressArea = wrapper.querySelector(".progress-area"),
      progressBar = progressArea.querySelector(".progress-bar"),
      musicList = wrapper.querySelector(".music-list"),
      moreMusicBtn = wrapper.querySelector("#more-music"),
      closemoreMusic = musicList.querySelector("#close");

    let musicIndex = Math.floor(Math.random() * allMusic.length + 1);
    isMusicPaused = true;

    window.addEventListener("load", () => {
      loadMusic(musicIndex);
      playingSong();
    });

    function loadMusic(indexNumb) {
      musicName.innerText = allMusic[indexNumb - 1].name;
      musicArtist.innerText = allMusic[indexNumb - 1].artist;
      let src = allMusic[indexNumb - 1].src;
      // musicImg.src = `images/${allMusic[indexNumb - 1].src}.jpg`;
      const audio = new Audio();
      audio.addEventListener('canplaythrough', function() {
        mainAudio.src = audio.src;
      });
      audio.src = `songs/${src}`; // Assume the file has no extension
    }

    //play music function
    function playMusic() {
      wrapper.classList.add("paused");
      playPauseBtn.querySelector("i").innerText = "pause";
      mainAudio.play();
    }

    //pause music function
    function pauseMusic() {
      wrapper.classList.remove("paused");
      playPauseBtn.querySelector("i").innerText = "play_arrow";
      mainAudio.pause();
    }

    //prev music function
    function prevMusic() {
      musicIndex--; //decrement of musicIndex by 1
      musicIndex < 1 ? (musicIndex = allMusic.length) : (musicIndex = musicIndex);
      loadMusic(musicIndex);
      playMusic();
      playingSong();
    }

    //next music function
    function nextMusic() {
      musicIndex++; //increment of musicIndex by 1
      musicIndex > allMusic.length ? (musicIndex = 1) : (musicIndex = musicIndex);
      loadMusic(musicIndex);
      playMusic();
      playingSong();
    }

    // play or pause button event
    playPauseBtn.addEventListener("click", () => {
      const isMusicPlay = wrapper.classList.contains("paused");
      isMusicPlay ? pauseMusic() : playMusic();
      playingSong();
    });

    //prev music button event
    prevBtn.addEventListener("click", () => {
      prevMusic();
    });

    //next music button event
    nextBtn.addEventListener("click", () => {
      nextMusic();
    });

    // update progress bar width according to music current time
    mainAudio.addEventListener("timeupdate", (e) => {
      const currentTime = e.target.currentTime;
      const duration = e.target.duration;
      let progressWidth = (currentTime / duration) * 100;
      progressBar.style.width = `${progressWidth}%`;

      let musicCurrentTime = wrapper.querySelector(".current-time"),
        musicDuartion = wrapper.querySelector(".max-duration");
      mainAudio.addEventListener("loadeddata", () => {
        // update song total duration
        let mainAdDuration = mainAudio.duration;
        let totalMin = Math.floor(mainAdDuration / 60);
        let totalSec = Math.floor(mainAdDuration % 60);
        if (totalSec < 10) {
          //if sec is less than 10 then add 0 before it
          totalSec = `0${totalSec}`;
        }
        musicDuartion.innerText = `${totalMin}:${totalSec}`;
      });
      // update playing song current time
      let currentMin = Math.floor(currentTime / 60);
      let currentSec = Math.floor(currentTime % 60);
      if (currentSec < 10) {
        //if sec is less than 10 then add 0 before it
        currentSec = `0${currentSec}`;
      }
      musicCurrentTime.innerText = `${currentMin}:${currentSec}`;
    });

    progressArea.addEventListener("click", (e) => {
      let progressWidth = progressArea.clientWidth;
      let clickedOffsetX = e.offsetX;
      let songDuration = mainAudio.duration;

      mainAudio.currentTime = (clickedOffsetX / progressWidth) * songDuration;
      playMusic(); //calling playMusic function
      playingSong();
    });

    //change loop, shuffle, repeat icon onclick
    const repeatBtn = wrapper.querySelector("#repeat-plist");
    repeatBtn.addEventListener("click", () => {
      let getText = repeatBtn.innerText; //getting this tag innerText
      switch (getText) {
        case "repeat":
          repeatBtn.innerText = "repeat_one";
          repeatBtn.setAttribute("title", "Song looped");
          break;
        case "repeat_one":
          repeatBtn.innerText = "shuffle";
          repeatBtn.setAttribute("title", "Playback shuffled");
          break;
        case "shuffle":
          repeatBtn.innerText = "repeat";
          repeatBtn.setAttribute("title", "Playlist looped");
          break;
      }
    });

    //code for what to do after song ended
    mainAudio.addEventListener("ended", () => {
      let getText = repeatBtn.innerText; //getting this tag innerText
      switch (getText) {
        case "repeat":
          nextMusic(); //calling nextMusic function
          break;
        case "repeat_one":
          mainAudio.currentTime = 0;
          loadMusic(musicIndex);
          playMusic();
          break;
        case "shuffle":
          let randIndex = Math.floor(Math.random() * allMusic.length + 1); //genereting random index/numb with max range of array length
          do {
            randIndex = Math.floor(Math.random() * allMusic.length + 1);
          } while (musicIndex == randIndex); //this loop run until the next random number won't be the same of current musicIndex
          musicIndex = randIndex; //passing randomIndex to musicIndex
          loadMusic(musicIndex);
          playMusic();
          playingSong();
          break;
      }
    });

    //show music list onclick of music icon
    moreMusicBtn.addEventListener("click", () => {
      musicList.classList.toggle("show");
    });
    closemoreMusic.addEventListener("click", () => {
      moreMusicBtn.click();
    });

    const ulTag = wrapper.querySelector("ul");

    // play particular song from the list onclick of li tag
    function playingSong() {
      const allLiTag = ulTag.querySelectorAll("li");

      for (let j = 0; j < allLiTag.length; j++) {
        let audioTag = allLiTag[j].querySelector(".audio-duration");

        if (allLiTag[j].classList.contains("playing")) {
          allLiTag[j].classList.remove("playing");
          let adDuration = audioTag.getAttribute("t-duration");
          audioTag.innerText = adDuration;
        }

        //if the li tag index is equal to the musicIndex then add playing class in it
        if (allLiTag[j].getAttribute("li-index") == musicIndex) {
          allLiTag[j].classList.add("playing");
          audioTag.innerText = "Playing";
        }

        allLiTag[j].setAttribute("onclick", "clicked(this)");
      }
    }

    //particular li clicked function
    function clicked(element) {
      let getLiIndex = element.getAttribute("li-index");
      musicIndex = getLiIndex; //updating current song index with clicked li index
      loadMusic(musicIndex);
      playingSong();
      playMusic();
    }

    // Step 1: Add event listener to input file element
    const uploadInput = document.getElementById('music-file');
    uploadInput.addEventListener('change', function() {
        const file = this.files[0];
        const songName = file.name.replace(/\.[^/.]+$/, ''); // Remove file extension
        const artist = "Unknown"; // You can set this dynamically if you have artist information
        const src = songName.replace(/\s+/g, '-').toLowerCase(); // Create a URL-friendly version of the song name
        
        // Step 2: Create a new entry in the allMusic array
        const newSong = {
            name: songName,
            artist: artist,
            src: src
        };

        // Step 3: Add the new song to the allMusic array
        allMusic.push(newSong);

        // Step 4: Append a new <li> element to the music list
        const ulTagMusic = wrapper.querySelector("ul");
        let liTagMusic = `<li li-index="${allMusic.length}">
                    <div class="row">
                      <span>${songName}</span>
                      <p>${artist}</p>
                      <button class="remove-music">remove<button>
                    </div>
                    <span id="${src}" class="audio-duration">0:00</span>
                    <audio class="${src}" src="${URL.createObjectURL(file)}"></audio>
                  </li>`;
        ulTagMusic.insertAdjacentHTML("beforeend", liTagMusic);

        // Step 5: Add an event listener to the newly created <li> element
        const newLi = ulTagMusic.lastElementChild;
        newLi.addEventListener("click", function() {
            clicked(this);
        });

        // Step 6: Load and play the uploaded song
        loadMusic(allMusic.length);
        playMusic();
    });