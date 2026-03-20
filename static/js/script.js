

document.querySelectorAll(".range").forEach(range => {
  const input = document.getElementById(range.dataset.target);

  range.addEventListener("input", () => {
    input.value = range.value;
  });

  input.addEventListener("input", () => {
    range.value = input.value;
  });
});

const btnOpen = document.querySelector(".start-calc-btn");
const btnClose = document.querySelector(".calc-btn");
const modal = document.querySelector(".calc-mass-wrap");
const mainText = document.querySelector(".main-text");
/* відкрити */
btnOpen.addEventListener("click", () => {
  modal.classList.remove("hidden");
  mainText.classList.add("hidden");
});

/* закрити */
btnClose.addEventListener("click", () => {
  modal.classList.add("hidden");
  mainText.classList.remove("hidden");
});