document.addEventListener("DOMContentLoaded", pomodoroModeOn);
document.getElementById("startButton").addEventListener("click", startTimer);
document.getElementById("pauseButton").addEventListener("click", pauseTimer);
document.getElementById("resetButton").addEventListener("click", resetTimer);

var pomodoroButton = document.getElementById("pomodoroModeButton");
pomodoroButton.addEventListener("click", pomodoroModeOn);
var shortBreakButton = document.getElementById("shortBreakModeButton");
shortBreakButton.addEventListener("click", shortBreakModeOn);
var longBreakButton = document.getElementById("longBreakModeButton");
longBreakButton.addEventListener("click", longBreakModeOn);

var countdownMins = 0;
var countdownSecs = 0;
var timeRemaining;
var countdownClock;
var currentTimer;
var pomodoroMinutes;
var shortBreakMinutes;
var longBreakMinutes;

if (pomodoroButton.value <= 0) {
    pomodoroMinutes = 25
} else {
    pomodoroMinutes = pomodoroButton.value
}

if (shortBreakButton.value <= 0) {
    shortBreakMinutes = 5
} else {
    shortBreakMinutes = shortBreakButton.value;
}

if (longBreakButton.value <= 0) {
    longBreakMinutes = 10
} else {
    longBreakMinutes = longBreakButton.value;
}

function pomodoroModeOn() {
    // In case the timer was running, stop countdownClock function
    clearInterval(countdownClock);

    // Reset time and timer display
    countdownMins = pomodoroMinutes;
    countdownSecs = 0;
    resetTimer();

  // Set timer to Pomodoro
  currentTimer = "Pomodoro";
}

function shortBreakModeOn() {

  // check if Pomodoro mode is on and timer is running
  if (currentTimer == "Pomodoro" && timeRemaining < (pomodoroMinutes * 60) && timeRemaining != 0) {
    if (pomodoroButton.value != false) {
      if (window.confirm("Are you sure you want to end your task early? You'll lose 10 points")) {

        //deduct 10 points from score
        $.ajax({
          url: '/deductPoints',
          success: function (data) {
            $("#score_span").html(data)
          }
        });

        // In case the timer was running, stop countdownClock function
        clearInterval(countdownClock);

        // Reset time and timer display
        countdownMins = shortBreakMinutes;
        countdownSecs = 0;
        resetTimer();

        // Set timer to Short Break
        currentTimer = "Short Break";
      }
    } else {
      // In case the timer was running, stop countdownClock function
      clearInterval(countdownClock);

      // Reset time and timer display
      countdownMins = shortBreakMinutes;
      countdownSecs = 0;
      resetTimer();

      // Set timer to Short Break
      currentTimer = "Short Break";
    }
  }
}
function longBreakModeOn() {
  // check if Pomodoro mode is on and timer is running
  if (currentTimer == "Pomodoro" && timeRemaining < (pomodoroMinutes * 60) && timeRemaining != 0) {
    if (pomodoroButton.value != false) {
      if (window.confirm("Are you sure you want to end your task early? You'll lose 10 points.")) {

        //deduct 10 points from score
        $.ajax({
          url: '/deductPoints',
          success: function (data) {
            $("#score_span").html(data)
          }
        });

        // In case the timer was running, stop countdownClock function
        clearInterval(countdownClock);

        // Reset time and timer display
        countdownMins = longBreakMinutes;
        countdownSecs = 0;
        resetTimer();

        // Set timer to Short Break
        currentTimer = "Long Break";
      }
    } else {
      // In case the timer was running, stop countdownClock function
      clearInterval(countdownClock);

      // Reset time and timer display
      countdownMins = longBreakMinutes;
      countdownSecs = 0;
      resetTimer();

      // Set timer to Short Break
      currentTimer = "Long Break";
    }
  }
}

function startTimer() {
  // Check to see if the timer has already been completed and reset if it has
  if (timeRemaining == 0) {
    resetTimer();
  }

  // Call countdownTimer function every second (1000ms)
  countdownClock = setInterval(function () { countdownTimer(); }, 1000);
}

function pauseTimer() {
  // Stop countdownClock function
  clearInterval(countdownClock);
}

function resetTimer() {
  // Stop the countdownClockfunction
  pauseTimer();

  // Reset the values
  document.getElementById('minsValue').textContent = countdownMins;
  document.getElementById('secsValue').textContent = '00';
  timeRemaining = (countdownMins * 60) + countdownSecs;

  // Display the reset time and title
  displayTimer();
  document.title = "Pomodoro Posse Timer";
}

function displayTimer() {

  var temp = timeRemaining;

  // Calculate the minute and second values
  var minutesValue = Math.floor(temp / 60);
  var secondsValue = temp % 60;

  // Pad the number if needed (ex. 9 is padded to 09) to display properly
  var minutesString = padValue(minutesValue);
  var secondsString = padValue(secondsValue);

  // Update the countdown values on the screen and title
  document.getElementById('minsValue').textContent = minutesString;
  document.getElementById('secsValue').textContent = secondsString;
  document.title = "(" + minutesString + ":" + secondsString + ") - " + currentTimer;
};

function padValue(integerValue) {
  if (integerValue > 9) {
    return integerValue.toString();
  }
  else {
    return '0' + integerValue.toString();
  }
}

function countdownTimer() {
  timeRemaining--;
  displayTimer();

  // If time is up, stop the timer and display notification
  if (timeRemaining == 0 && currentTimer == "Pomodoro") {

    document.title = "Time is up!";
    pauseTimer();

    // add points to score
    $.ajax({
      url: '/addPoints',
      success: function (data) {
        $("#score_span").html(data)
      }
    });

    setTimeout(function () {
      alert("Congrats! You won 10 points for completing your task!");
    }, 0)

  }
  else if (timeRemaining == 0) {
    pauseTimer();
  }
}