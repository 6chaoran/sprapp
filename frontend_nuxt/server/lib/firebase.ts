import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

//your firebase configuration goes here
//https://firebase.google.com/docs/web/learn-more?authuser=0&hl=en#modular-version

const firebaseConfig = {
    apiKey: "AIzaSyBABCJoHV9hf3MlEmH_xB5eZax3OHWlcS0",
    authDomain: "sgprapp.firebaseapp.com",
    projectId: "sgprapp",
    storageBucket: "sgprapp.appspot.com",
    messagingSenderId: "452990261863",
    appId: "1:452990261863:web:59983f7958ab6295dd92c2",
    measurementId: "G-FG3L7LZ5CN"
  };

export const firebaseApp = initializeApp(firebaseConfig);

export const firestoreDb = getFirestore(firebaseApp);