
function truncateString(str, maxLength) {
    return str.length > maxLength ? str.slice(0, maxLength - 3) + '...' : str;
}

const customTrack = document.getElementById("custom-track");
customTrack.addEventListener("keyup", ({ key }) => {
    if (key === "Enter") {
        eel.download_track(customTrack.value)();
        customTrack.value = "";
    }
});

async function loadTracks() {
    const tracks = await eel.get_tracks()();
    const tracksNode = document.getElementById("tracks");
    const trackTemplate = document.getElementById("track-template");

    if (Object.keys(tracks).length === 0) {
        loadTracks();
    }

    for (const track of tracks) {
        const trackObject = track["track"];
        const newTrack = trackTemplate.cloneNode(true);

        const newTrackImage = trackObject["artwork_url"] || "/img/notfound.png";
        newTrack.querySelector("img").src = newTrackImage;

        newTrack.querySelector(".track-name").textContent = truncateString(trackObject["title"], 20);
        newTrack.querySelector(".track-author").textContent = truncateString(trackObject["user"]["username"], 8);

        const trackDownload = newTrack.querySelector(".track-download");
        const trackExists = await eel.track_exists(trackObject["title"])();
        
        if (trackExists) {
            trackDownload.disabled = true;
            trackDownload.textContent = "Downloaded";
        } else {
            trackDownload.addEventListener("click", async () => {
                trackDownload.disabled = true;
                trackDownload.textContent = "Downloading";
                const result = await eel.download_track(trackObject["permalink_url"])();
                trackDownload.textContent = result ? "Downloaded" : "Download";
                trackDownload.disabled = result;
            });
        }

        newTrack.removeAttribute("id");
        newTrack.style.display = 'flex';
        tracksNode.appendChild(newTrack);
    }
}

window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if (scrollTop + clientHeight >= scrollHeight) {
        eel.create_notification("Loading tracks", "Loading more tracks", "/img/logo.png");
        loadTracks();
    }
});

window.addEventListener("load", () => {
    eel.set_original_url();
    loadTracks();
});
