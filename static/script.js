var numericFields = ["age", "bp", "chol", "maxhr", "oldpeak"];

// remove error highlight when user starts typing
numericFields.forEach(function(id) {
    document.getElementById(id).addEventListener("input", function() {
        this.classList.remove("error");
    });
});

document.getElementById("predForm").addEventListener("submit", function(e) {
    e.preventDefault();

    // simple validation
    var valid = true;
    numericFields.forEach(function(id) {
        var el = document.getElementById(id);
        if (el.value === "" || isNaN(el.value)) {
            el.classList.add("error");
            valid = false;
        }
    });
    if (!valid) return;

    var btn = document.getElementById("submitBtn");
    btn.disabled = true;
    btn.innerHTML = '<span class="dots">Analyzing</span>';

    // hide old result
    var box = document.getElementById("result");
    box.className = "";
    box.style.display = "none";
    box.style.opacity = "0";

    var data = {
        age:     document.getElementById("age").value,
        bp:      document.getElementById("bp").value,
        chol:    document.getElementById("chol").value,
        fasting: document.getElementById("fasting").value,
        maxhr:   document.getElementById("maxhr").value,
        oldpeak: document.getElementById("oldpeak").value,
        sex:     document.getElementById("sex").value,
        chest:   document.getElementById("chest").value,
        ecg:     document.getElementById("ecg").value,
        angina:  document.getElementById("angina").value,
        slope:   document.getElementById("slope").value
    };

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(function(res) { return res.json(); })
    .then(function(json) {
        btn.disabled = false;
        btn.textContent = "Predict Again";

        var isPositive = json.result.includes("Detected") && !json.result.includes("No Heart");

        box.innerHTML =
            '<span class="icon">' + (isPositive ? "&#9888;" : "&#10003;") + '</span>' +
            json.result +
            '<small>This is a model prediction. Please consult a doctor for medical advice.</small>';

        box.className = isPositive ? "positive" : "negative";
        box.style.display = "block";

        // trigger fade-in
        setTimeout(function() {
            box.style.opacity = "1";
        }, 10);

        box.scrollIntoView({ behavior: "smooth", block: "center" });
    })
    .catch(function(err) {
        btn.disabled = false;
        btn.textContent = "Predict";
        alert("Something went wrong. Make sure Flask is running.\n" + err);
    });
});
