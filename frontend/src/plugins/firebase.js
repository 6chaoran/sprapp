// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics, logEvent } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBABCJoHV9hf3MlEmH_xB5eZax3OHWlcS0",
  authDomain: "sgprapp.firebaseapp.com",
  projectId: "sgprapp",
  storageBucket: "sgprapp.appspot.com",
  messagingSenderId: "452990261863",
  appId: "1:452990261863:web:59983f7958ab6295dd92c2",
  measurementId: "G-FG3L7LZ5CN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { analytics, logEvent };