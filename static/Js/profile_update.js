// Toggle internship details
const internshipSelect = document.getElementById("internship");
const internshipDetails = document.getElementById("internshipDetails");
internshipSelect.addEventListener("change", function () {
  if (this.value === "yes") {
    internshipDetails.style.display = "block";
  } 
  else {
    internshipDetails.style.display = "none";
  }
});

// Toggle location input
const panIndiaRadio = document.getElementById("PANLocation");
const otherLocationRadio = document.getElementById("otherLocation");
const locationInputContainer = document.getElementById("locationInputContainer");

panIndiaRadio.addEventListener("change", function () {
  if (this.checked) {
    locationInputContainer.style.display = "none";
  }
});

otherLocationRadio.addEventListener("change", function () {
  if (this.checked) {
    locationInputContainer.style.display = "block";
  }
});

// Initialize form based on existing values (if any)
document.addEventListener("DOMContentLoaded", function () {
  // Trigger change events to set initial visibility
  internshipSelect.dispatchEvent(new Event("change"));

  if (otherLocationRadio.checked) {
    locationInputContainer.style.display = "block";
  }
});

// Project Hide and display
const projectSelect = document.getElementById("project");
const projectHide = document.getElementById("projectHide");

// Function to toggle project details
function toggleProjectDetails() {
  if (projectSelect.value === "yes") {
    projectHide.style.display = "block";
  } else {
    projectHide.style.display = "none";
  }
}

// Run toggle on page load
document.addEventListener("DOMContentLoaded", function () {
  toggleProjectDetails();
});

// Also toggle when user changes the selection
projectSelect.addEventListener("change", toggleProjectDetails);

