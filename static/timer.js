// Retrieve the countdown date from session storage or set it to now + 1 minute

var countDownDate = sessionStorage.getItem('countDownDate');

if (!countDownDate) {
    countDownDate = new Date();
    countDownDate.setSeconds(countDownDate.getSeconds() + 2403); // Set seconds instead of minutes
    sessionStorage.setItem('countDownDate', countDownDate);
} else {
    countDownDate = new Date(countDownDate);
}

// Set an interval to update the timer every second
var x = setInterval(function() {
    var now = new Date().getTime();
    var distance = countDownDate - now;

    // Check if the "timer" element exists before updating its content
    var timerElement = document.getElementById("timer");
    if (timerElement) {
        // Calculate minutes and seconds remaining
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Set color based on remaining time
        var color = (minutes === 0 && seconds <= 30) ? "red" : "green";

        // Display the timer with color
        timerElement.innerHTML = `<p><span style="color: blue;">TIME:</span> <span style="color: ${color};">${minutes}m ${seconds}s</span>`;
    }

    // Notify when 5 minutes remaining
    if (minutes === 0 && seconds === 300) {
        showNotification("Hurry Up! 5 minutes remaining!");
    }

    if (distance < 0) {
        clearInterval(x);
        // Display a message when time is up
        document.getElementById("timer").innerHTML = "Time's Up! Thank you for Giving Us a Trial!!";

        // Redirect to the results page
        window.location.href = "/results"; 
    }
}, 1000);

// Function to show a customized notification
function showNotification(message) {
    // Show custom notification at the top of the page
    var notificationContainer = document.getElementById("customNotification");
    if (notificationContainer) {
        // Update notification content
        notificationContainer.innerHTML = message;

        // Show the notification container
        notificationContainer.style.display = "block";

        // Hide the notification after a certain duration (e.g., 5 seconds)
        setTimeout(function() {
            notificationContainer.style.display = "none";
        }, 3000); // 3000 milliseconds = 5 seconds
    }

    // Check if the browser supports the Notification API
    if (Notification && Notification.permission === "granted") {
        var options = {
            body: message, // Notification content
            icon: "../static/images/bell.png", // URL of the notification icon
        };

        var notification = new Notification("Quiz Timer", options);

        // You can add an event listener for further customization, e.g., clicking on the notification
        notification.addEventListener("click", function() {
            // Perform any action when the user clicks on the notification
            console.log("Notification clicked!");
        });
    } else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission().then(function(permission) {
            if (permission === "granted") {
                showNotification(message);
            }
        });
    }
}

// Function to move to the next question by submitting the form
function nextQuestion() {
    document.getElementById("quizForm").submit(); // Submit the form
}

// Function to reset the timer
function resetTimer() {
    // Clear sessionStorage when resetting the timer
    sessionStorage.clear();

    countDownDate = new Date();
    countDownDate.setSeconds(countDownDate.getSeconds() + 2403);
    sessionStorage.setItem('countDownDate', countDownDate);

    var now = new Date().getTime();
    var distance = countDownDate - now;

    // Calculate minutes and seconds remaining
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the timer
    document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s ";
}
