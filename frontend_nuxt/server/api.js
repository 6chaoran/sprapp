// Import Axios
import axios from 'axios';

// Define the base URL for your API (if applicable)
const BASE_URL = 'https://backend-dot-sgprapp.et.r.appspot.com/api/v2';
// const BASE_URL = 'http://localhost:8000/api/v2';

// Export the function that makes the GET request
export const fetchData = async (endpoint, params= null) => {
  try {
    // Make the GET request using Axios
    const response = await axios.get(`${BASE_URL}${endpoint}`,{
      params: params
    });

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

// Export the function that makes the GET request
export const putData = async (endpoint, params) => {
  try {
    // Make the GET request using Axios
    const response = await axios.put(`${BASE_URL}${endpoint}`, null, {
      params: params, headers: {
        'Accept': 'application/json'
    }})
    // Return the data from the response
    return response.data;
  } catch (error) {
    // Handle any errors that occur during the request
    console.error('Error putting data:', error);
    throw error;
  }
};

export const delData = async (endpoint, data) => {
  try {
    // Make the GET request using Axios
    const response = await axios.delete(`${BASE_URL}${endpoint}`, {
      data: data
    })
    // Return the data from the response
    return response.data;
  } catch (error) {
    // Handle any errors that occur during the request
    console.error('Error deleting data:', error);
    throw error;
  }
};
