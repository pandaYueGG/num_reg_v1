document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const resultDiv = document.getElementById("result");

  fetch("http://localhost:5000/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      resultDiv.innerHTML = `<p>Predicted Number: ${data.digit}</p>`;
    })
    .catch((error) => {
      resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    });
});
