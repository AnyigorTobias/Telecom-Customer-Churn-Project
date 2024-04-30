// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault(); // Prevent default form submission behavior
    
    // Get form data
    const formData = {
        gender: document.getElementById('gender').value,
        seniorcitizen: parseInt(document.getElementById('seniorcitizen').value),
        partner: parseInt(document.getElementById('partner').value),
        dependents: parseInt(document.getElementById('dependents').value),
        phoneservice: parseInt(document.getElementById('phoneservice').value),
        multiplelines: parseInt(document.getElementById('multiplelines').value),
        internetservice: parseInt(document.getElementById('internetservice').value),
        onlinesecurity: parseInt(document.getElementById('onlinesecurity').value),
        onlinebackup: parseInt(document.getElementById('onlinebackup').value),
        deviceprotection: parseInt(document.getElementById('deviceprotection').value),
        techsupport: parseInt(document.getElementById('techsupport').value),
        streamingtv: parseInt(document.getElementById('streamingtv').value),
        streamingmovies: parseInt(document.getElementById('streamingmovies').value),
        contract: document.getElementById('contract').value,
        paperlessbilling: document.getElementById('paperlessbilling').value,
        paymentmethod: document.getElementById('paymentmethod').value,
        tenure: parseInt(document.getElementById('tenure').value),
        monthlycharges: parseFloat(document.getElementById('monthlycharges').value),
        totalcharges: parseFloat(document.getElementById('totalcharges').value)
    };
    
    // Send form data to server for prediction
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Determine churn prediction result
        let predictionMessage;
        if (data.prediction >= 0.5) {
            predictionMessage = 'Customer is likely to churn. Send a marketing message to retain them.';
        } else {
            predictionMessage = 'Customer can stay. No immediate action required.';
        }
        
        // Display prediction result message
        showMessage(predictionMessage);
    })
    .catch(error => {
        // Display error message
        showMessage('An error occurred. Please try again.');
    });
    
    // Display loading message
    showMessage('Loading...');
}

// Function to display messages in the message container
function showMessage(message) {
    const messageContainer = document.querySelector('.message-container');
    messageContainer.innerHTML = `<h2>${message}</h2>`;
}

// Add event listener to form submit button
document.querySelector('form').addEventListener('submit', handleSubmit);
