// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBIKKYEhD6xR0ECY7XJaXHY5_iwvt90iL8",
  authDomain: "inventory-management-e5336.firebaseapp.com",
  projectId: "inventory-management-e5336",
  storageBucket: "inventory-management-e5336.appspot.com",
  messagingSenderId: "138252161941",
  appId: "1:138252161941:web:174c9731863312e42d1c9c",
  measurementId: "G-SFNQ63SP8C"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const firestore = getFirestore(app);
const storage = getStorage(app);

export {firestore, storage}