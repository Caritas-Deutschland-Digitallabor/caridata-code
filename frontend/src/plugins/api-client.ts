import axios from "axios";
import { AppClient } from "../services/AppClient";

axios.defaults.xsrfHeaderName = "x-csrf-token";
axios.defaults.xsrfCookieName = "caridata_csrf_token";
axios.defaults.withXSRFToken = true;

export default new AppClient({
  BASE: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  WITH_CREDENTIALS: true,
});
