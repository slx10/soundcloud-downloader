eel.expose(createNotification);

function createNotification(title, description, img) {
    const notifications = document.getElementById("notifications");
    const notificationTemplate = document.getElementById("notification-template");
    const newNotification = notificationTemplate.cloneNode(true);
    newNotification.querySelector("img").src = img
    newNotification.querySelector(".notification-title").textContent = title;
    newNotification.querySelector(".notification-description").textContent = description;
    newNotification.removeAttribute("id");

    notifications.appendChild(newNotification);
    setTimeout(() => {
        newNotification.classList.add("show");
    }, 10);

    setTimeout(() => {
        newNotification.classList.remove("show");

        setTimeout(() => {
            newNotification.remove();
        }, 500);
    }, 2000);
}
