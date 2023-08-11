// Import Axios
import axios from 'axios';

// Define the base URL for your API (if applicable)
const BASE_URL = 'https://backend-dot-sgprapp.et.r.appspot.com/';

// Export the function that makes the GET request
export const fetchData = async (endpoint) => {
  try {
    // Make the GET request using Axios
    const response = await axios.get(`${BASE_URL}${endpoint}`);

    // Return the data from the response
    return response.data;
  } catch (error) {
    // Handle any errors that occur during the request
    console.error('Error fetching data:', error);
    throw error;
  }
};


// Export the function that makes the GET request
export const postData = async (endpoint, params) => {
  try {
    // Make the GET request using Axios
    const response = await axios.post(`${BASE_URL}${endpoint}`, null, {
      params: params, headers: {
        'Accept': 'application/json'
    }})
    // Return the data from the response
    return response.data;
  } catch (error) {
    // Handle any errors that occur during the request
    console.error('Error posting data:', error);
    throw error;
  }
};

