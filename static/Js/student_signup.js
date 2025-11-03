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
