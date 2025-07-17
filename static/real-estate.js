document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('prediction-result');
    
    // Type search enhancement
    const typeInput = document.getElementById('type');
    if (typeInput) {
        typeInput.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const options = document.querySelectorAll('#type-options option');
            
            let matchCount = 0;
            options.forEach(option => {
                if (option.value.toLowerCase().includes(value)) {
                    matchCount++;
                }
            });
            
            if (value && matchCount > 0) {
                this.classList.add('valid-input');
                this.classList.remove('invalid-input');
            } else if (value) {
                this.classList.add('invalid-input');
                this.classList.remove('valid-input');
            } else {
                this.classList.remove('valid-input', 'invalid-input');
            }
        });
    }
    
    // Set default values for easier testing
    document.getElementById('area').value = '450';
    document.getElementById('bedrooms').value = '0';
    document.getElementById('bath').value = '1';
    document.getElementById('initial_amount').value = '0';
    document.getElementById('monthly_installment').value = '0';
    document.getElementById('remaining_installments').value = '0';
    document.getElementById('location').value = 'Wazirabad Road';
    document.getElementById('location_city').value = 'Sambrial';
    document.getElementById('location_province').value = 'Punjab';
    
    if (typeInput) {
        typeInput.value = 'Office';
    }
    
    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        console.log("Form submitted!"); // Debug log
        
        // Get the purpose value (radio button)
        const purposeRadio = document.querySelector('input[name="purpose"]:checked');
        if (!purposeRadio) {
            alert('Please select a purpose (For Sale or For Rent)');
            return;
        }
        
        // Show loading indicator immediately
        if (!resultDiv) {
            console.error("Result div not found!");
            return;
        }
        
        resultDiv.className = 'prediction-result';
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <div class="loading-spinner"></div>
                <p>Calculating property price...</p>
                <p style="font-size: 12px; color: #666; margin-top: 10px;">This may take a few seconds...</p>
            </div>
        `;
        
        // Get form values
        const formData = {
            type: document.getElementById('type').value,
            area: parseFloat(document.getElementById('area').value),
            purpose: purposeRadio.value,
            bedrooms: parseFloat(document.getElementById('bedrooms').value),
            bath: parseFloat(document.getElementById('bath').value),
            initial_amount: parseFloat(document.getElementById('initial_amount').value) || 0,
            monthly_installment: parseFloat(document.getElementById('monthly_installment').value) || 0,
            remaining_installments: parseInt(document.getElementById('remaining_installments').value) || 0,
            location: document.getElementById('location').value,
            location_city: document.getElementById('location_city').value,
            location_province: document.getElementById('location_province').value
        };
        
        console.log("Sending data:", formData);
        
        try {
            // Add timeout to prevent hanging
            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Request timeout after 30 seconds')), 30000)
            );
            
            const fetchPromise = fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            // Race between fetch and timeout
            const response = await Promise.race([fetchPromise, timeoutPromise]);
            
            console.log("Response status:", response.status);
            console.log("Response ok:", response.ok);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error("Server error response:", errorText);
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }
            
            const data = await response.json();
            console.log("Response received:", data);
            
            if (data.success) {
                const predictedPrice = parseFloat(data.prediction);
                
                resultDiv.className = 'prediction-result result-success';
                resultDiv.innerHTML = `
                    <div style="text-align: center; padding: 20px;">
                        <h3 style="color: #10b981; margin-bottom: 15px;">
                            <i class="fas fa-check-circle"></i> Prediction Complete
                        </h3>
                        <div class="prediction-value" style="font-size: 2em; font-weight: bold; color: #2563eb; margin: 15px 0;">
                            ₨ ${predictedPrice.toLocaleString('en-IN', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            })} Lakhs
                        </div>
                        <p style="color: #6b7280; margin-bottom: 15px;">
                            (Approximately ₨ ${(predictedPrice * 100000).toLocaleString('en-IN')})
                        </p>
                        <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin-top: 20px;">
                            <p style="font-size: 14px; color: #6b7280; margin: 0;">
                                <i class="fas fa-robot"></i> Prediction from trained ML model
                            </p>
                        </div>
                    </div>
                `;
            } else {
                throw new Error(data.error || 'Error processing prediction');
            }
        } catch (error) {
            console.error("Error details:", error);
            resultDiv.className = 'prediction-result result-error';
            resultDiv.innerHTML = `
                <div style="text-align: center; padding: 20px;">
                    <h3 style="color: #ef4444; margin-bottom: 15px;">
                        <i class="fas fa-exclamation-triangle"></i> Prediction Failed
                    </h3>
                    <p style="color: #ef4444; margin-bottom: 10px;">
                        ${error.message || 'Unknown error occurred'}
                    </p>
                    <p style="color: #6b7280; font-size: 14px;">
                        Please check your inputs and try again.
                    </p>
                    <button onclick="location.reload()" style="
                        background: #2563eb; 
                        color: white; 
                        border: none; 
                        padding: 10px 20px; 
                        border-radius: 6px; 
                        cursor: pointer; 
                        margin-top: 15px;
                    ">
                        Refresh Page
                    </button>
                </div>
            `;
        }
    });
});