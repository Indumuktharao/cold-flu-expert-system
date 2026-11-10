const symptomInputs = document.querySelectorAll('input[name="symptoms"]');
const count = document.getElementById('count');

function updateCount() {
  if (!count) return;
  const total = [...symptomInputs].filter(input => input.checked).length;
  count.innerHTML = `${total}<small>selected</small>`;
}

symptomInputs.forEach(input => input.addEventListener('change', updateCount));
updateCount();

const results = document.getElementById('results');
if (results) results.scrollIntoView({ behavior: 'smooth', block: 'start' });
