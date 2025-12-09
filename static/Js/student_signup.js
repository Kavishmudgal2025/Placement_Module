fetch(statesUrl)
  .then(res => res.json())
  .then(states => {
    console.log(states);  
    const select = document.getElementById("state");
    states.forEach(state => {
      let option = document.createElement("option");
      option.value = state.name;
      option.textContent = state.name;
      select.appendChild(option);
    });
  })
  .catch(err => console.error("Error loading JSON:", err));

// Load universities from JSON file
fetch("/static/Json/universities.json")
    .then(response => response.json())
    .then(data => {
        const dropdown = document.getElementById("university");

        data.forEach(university => {
            let option = document.createElement("option");
            option.value = university;
            option.textContent = university;
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error("Error loading university list:", error));

// Load Specializations
fetch(specializationsUrl)
    .then(res => res.json())
    .then(data => {
        const specDropdown = document.getElementById("spec");

        data.forEach(spec => {
            let option = document.createElement("option");
            option.value = spec;
            option.textContent = spec;
            specDropdown.appendChild(option);
        });
    })
    .catch(err => console.error("Error loading Specialization JSON:", err));

