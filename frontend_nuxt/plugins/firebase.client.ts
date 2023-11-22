import { defineNuxtPlugin } from '#app'
import { initializeApp } from 'firebase/app'
import { getAuth } from "firebase/auth"
import { getFirestore } from 'firebase/firestore'
import { getAnalytics } from "firebase/analytics"

export default defineNuxtPlugin(nuxtApp => {
  // const config = useRuntimeConfig()
  const firebaseConfig = {
    apiKey: "AIzaSyBABCJoHV9hf3MlEmH_xB5eZax3OHWlcS0",
    authDomain: "sgprapp.firebaseapp.com",
    projectId: "sgprapp",
    storageBucket: "sgprapp.appspot.com",
    messagingSenderId: "452990261863",
    appId: "1:452990261863:web:59983f7958ab6295dd92c2",
    measurementId: "G-FG3L7LZ5CN"
  };
  const app = initializeApp(firebaseConfig)
  const analytics = getAnalytics(app)
  const auth = getAuth(app)
  const firestore = getFirestore(app)

  nuxtApp.vueApp.provide('auth', auth)
  nuxtApp.provide('auth', auth)

  nuxtApp.vueApp.provide('firestore', firestore)
  nuxtApp.provide('firestore', firestore)

  nuxtApp.vueApp.provide('analytics', analytics)
  nuxtApp.provide('analytics', analytics)
})