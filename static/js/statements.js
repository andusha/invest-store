
async function updateState(id, approve){
  await fetch('/admin/statements', {
      headers : {
          'Content-Type' : 'application/json'
      },
      method : 'POST',
      body : JSON.stringify( {
          'id' : id,
          'approve' : approve
      })
  })
}

// Toggle dropdown function
function dropdawnMenusFunc() {
  const dropdownBtns = document.querySelectorAll("#btn");
  const dropdownMenus = document.querySelectorAll("#dropdown");
  const toggleArrows = document.querySelectorAll("#arrow");
  const stateToggles = document.querySelectorAll("#stateToggle");
  const state = {0: ['bg-gray-100', 'не расмотренно'], 1: ['bg-main text-white', 'одобренно'], 2: ['bg-red-500 text-white', 'не одобренно']}
  for (let i = 0; i < dropdownBtns.length; i++) {
    const toggleDropdown = function () {
      dropdownMenus[i].classList.toggle("show");
      toggleArrows[i].classList.toggle("arrow");
    };

    let dropdownMenuButtons = dropdownMenus[i].childNodes
    let statementId = dropdownMenus[i].dataset.id
    let stateToggle = stateToggles[i]
    let dropdownBtn = dropdownBtns[i]
    dropdownMenuButtons.forEach(button => {
      button.addEventListener('click', () =>{
        updateState(statementId, button.dataset.flag)
        stateToggle.className = state[button.dataset.flag][0] + " p-4 rounded-r-lg w-1/3";
        dropdownBtn.firstElementChild.innerText = state[button.dataset.flag][1]
      })
    })
    // Toggle dropdown open/close when dropdown button is clicked
    dropdownBtns[i].addEventListener("click", function (e) {
      e.stopPropagation();
      toggleDropdown();
    });

    // Close dropdown when dom element is clicked
    document.documentElement.addEventListener("click", function () {
      if (dropdownMenus[i].classList.contains("show")) {
        toggleDropdown();
      }
    });
}};

dropdawnMenusFunc()