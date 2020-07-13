document.addEventListener("DOMContentLoaded", pomodoroModeOn);
document.getElementById("startButton").addEventListener("click", startTimer);
document.getElementById("pauseButton").addEventListener("click", pauseTimer);
document.getElementById("resetButton").addEventListener("click", resetTimer);
document.getElementById("pomodoroModeButton").addEventListener("click", pomodoroModeOn);
document.getElementById("shortBreakModeButton").addEventListener("click", shortBreakModeOn);
document.getElementById("longBreakModeButton").addEventListener("click", longBreakModeOn);

var countdownMins = 0;
var countdownSecs = 0;
var timeRemaining;
var countdownClock;
var currentTimer;
var pomodoroMinutes = 25;
var shortBreakMinutes = 5;
var longBreakMinutes = 10;

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
  // In case the timer was running, stop countdownClock function
  clearInterval(countdownClock);

  // Reset time and timer display
  countdownMins = shortBreakMinutes;
  countdownSecs = 0;
  resetTimer();

  // Set timer to Short Break
  currentTimer = "Short Break";
}

function longBreakModeOn() {
  // In case the timer was running, stop countdownClock function
  clearInterval(countdownClock);

  // Reset time and timer display
  countdownMins = longBreakMinutes;
  countdownSecs = 0;
  resetTimer();

  // Set timer to Long Break
  currentTimer = "Long Break";
}

function startTimer() {
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
  var secondsValue = temp %  60;

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
  timeRemaining --;
  displayTimer();

  // If time is up, stop the timer and display notification
  if (timeRemaining == 0 && currentTimer == "Pomodoro") {
    
    document.title = "Time is up!";
    pauseTimer();
    
    //increase score value if task is finished
    var scoreSpan = document.getElementById('score-span');
    var score = parseInt(scoreSpan.innerHTML);
    scoreSpan.innerHTML = score + 10;

    setTimeout(function () {
      alert("Congrats! You won 10 points for completing your task!");
    }, 0)
    
  }
  else if(timeRemaining == 0){
    pauseTimer();
  }
}