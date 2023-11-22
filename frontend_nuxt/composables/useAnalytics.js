import { logEvent } from "firebase/analytics";
export default function() {
  const { $analytics } = useNuxtApp()
  const logEventGA = (event, param = null) => {
    logEvent($analytics, event, param)
  }
  return { logEventGA }
};