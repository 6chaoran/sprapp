import { defineNuxtPlugin } from '#app'
import { initializeApp } from 'firebase/app'

export default defineNuxtPlugin(() => {
    const firebaseConfig = {
        apiKey: "AIzaSyBABCJoHV9hf3MlEmH_xB5eZax3OHWlcS0",
        authDomain: "sgprapp.firebaseapp.com",
        projectId: "sgprapp",
        storageBucket: "sgprapp.appspot.com",
        messagingSenderId: "452990261863",
        appId: "1:452990261863:web:59983f7958ab6295dd92c2",
        measurementId: "G-FG3L7LZ5CN"
      };
    const firebaseApp = initializeApp(firebaseConfig)

  return {
    provide: {
      firebaseApp,
    },
  }
})