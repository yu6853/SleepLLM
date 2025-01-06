const profession = document.getElementById('profession');
const gender = document.getElementById('gender');
const age = document.getElementById('age');
const sleep_quality = document.getElementById('sleep_quality');
const pressure_extent = document.getElementById('pressure_extent');
const step = document.getElementById('step');
const disorder = document.getElementById('disorder');
const file = document.getElementById('file');

function changeSVal() {
    sVal = parseInt(sleep_quality.value);
    const sValPercent = parseFloat(sVal, 2) / 10 * 100
    sleep_quality.style.background = `linear-gradient(to right, #00c3ffc3, white ${sValPercent}%, white`
}

function changePVal() {
    pVal = parseInt(pressure_extent.value);
    const pValPercent = parseFloat(pVal, 2) / 10 * 100
    pressure_extent.style.background = `linear-gradient(to right, #00c3ffc3, white ${pValPercent}%, white`
}

function submitFunction() {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    
    profVal = profession.value;
    gVal = gender.value;
    aVal = age.value;
    sVal = sleep_quality.value;
    pVal = pressure_extent.value;
    stepVal = step.value;
    dVal = disorder.value;
    fVal = file.files[0];
    // console.log(profVal);
    // console.log(gVal);
    // console.log(aVal);
    // console.log(sVal)
    // console.log(pVal);
    // console.log(stepVal);
    // console.log(dVal);
    // console.log(fVal);
    formData.append('file', fVal);
    formData.append("profession", profVal);
    formData.append("gender", gVal);
    formData.append("age", aVal);
    formData.append("sleep_quality", sVal);
    formData.append("pressure_extent", pVal);
    formData.append("step", stepVal);
    formData.append("disorder", dVal);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then((response) => {
        console.log('Redirected to: ', response.url);
        window.location.href = response.url;
    })
    .catch((error) => {console.error('上传出错', error);});
}  

document.getElementById('submit').addEventListener("click", submitFunction)