import React, { useState } from 'react';
function BloodReportForm() {
  const [showButton, setShowButton] = useState(false);
  const [formData, setFormData] = useState({
    fullname: '',
    age: '',
    gender: '',
    wbcCount: '',
    crpLevel: '',
    esrLevel: '',
    procalcitoninLevel: '',
    cough: 0,
    chills: 0,
    productiveCough: 0,
    chestPain: 0,
    fatigue: 0,
    shortnessOfBreath: 0
  });


  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    let newValue;
    if (type === 'checkbox') {
      newValue = checked ? 1 : 0;
    } else if (type === 'number') {
      newValue = parseFloat(value);
    } else {
      newValue = value;
    }
    setFormData(prevState => ({
      ...prevState,
      [name]: newValue
    }));
  };

  const handleSubmit = async(e) => {
    e.preventDefault();
    //console.log(formData);
    console.log(JSON.stringify(formData)) // You can send the form data to your server or perform further processing here
    const url = "http://127.0.0.1:5000/predict"
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log("Response from server:", data);
        
        // Handle the response data as needed
    } catch (error) {
        console.error("Error:", error);
        // Handle errors such as network errors, server errors, etc.
    }
    setShowButton(true);
  };


  return (<>
  <h1>PnuemoCare</h1>
    <form onSubmit={handleSubmit}>
      <label>
        Full Name:
        <input type="text" name="fullname" value={formData.fullname} onChange={handleChange} required={true} />
      </label>
      <br />
      <label>
        Age:
        <input type="number" name="age" value={formData.age} onChange={handleChange} required={true} />
      </label>
      <br />
      <label>
        Gender:
        <select name="gender" value={formData.gender} onChange={handleChange} required={true}>
          <option value="">Select Gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </label>
      <br />
      <label>
        WBC Count:
        <input type="number" name="wbcCount" value={formData.wbcCount} onChange={handleChange} required={true} />
      </label>
      <br />
      <label>
        CRP Level:
        <input type="number" name="crpLevel" value={formData.crpLevel} onChange={handleChange} required={true} />
      </label>
      <br />
      <label>
        ESR Level:
        <input type="number" name="esrLevel" value={formData.esrLevel} onChange={handleChange} required={true} />
      </label>
      <br />
      <label>
        Procalcitonin Level:
        <input type="number" name="procalcitoninLevel" value={formData.procalcitoninLevel} onChange={handleChange} />
      </label>
      <br />
      <label>
        Cough:
        <input type="checkbox" name="cough" checked={formData.cough} onChange={handleChange}  />
      </label>
      <br />
      <label>
        Chills:
        <input type="checkbox" name="chills" checked={formData.chills} onChange={handleChange}  />
      </label>
      <br />
      <label>
        Productive Cough:
        <input type="checkbox" name="productiveCough" checked={formData.productiveCough} onChange={handleChange}  />
      </label>
      <br />
      <label>
        Chest Pain:
        <input type="checkbox" name="chestPain" checked={formData.chestPain} onChange={handleChange} />
      </label>
      <br />
      <label>
        Fatigue:
        <input type="checkbox" name="fatigue" checked={formData.fatigue} onChange={handleChange} />
      </label>
      <br />
      <label>
        Shortness of Breath:
        <input type="checkbox" name="shortnessOfBreath" checked={formData.shortnessOfBreath} onChange={handleChange} />
      </label>
      <br />
      <button type="submit">Submit</button>
    </form>
    {showButton && (
        <button onClick={()=>setShowButton(false)}>Image detection</button>)}
    </>
  );
}

export default BloodReportForm;