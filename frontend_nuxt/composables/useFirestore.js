import { doc } from "firebase/firestore";
export default function () {
    const { $firestore } = useNuxtApp()
    const getDocs = () => {
        const alovelaceDocumentRef = doc($firestore, 'users', 'alovelace');
        console.log(alovelaceDocumentRef)
    }
    return { getDocs }
};